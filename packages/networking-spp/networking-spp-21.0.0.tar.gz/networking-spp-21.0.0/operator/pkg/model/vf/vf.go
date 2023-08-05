package vf

import (
	"encoding/json"
	"fmt"
	sppv1 "opendev.org/x/networking-spp/operator/pkg/apis/spp/v1"
	sppcommon "opendev.org/x/networking-spp/operator/pkg/model/common"
	"strconv"
	"strings"
)

// checkComponentsExist returns ture if vhost or ring exist in response
func CheckComponentsExist(response *sppv1.SppVfResponse) bool {
	for _, component := range response.Components {
		if component.Type != "unuse" {
			return true
		}
	}
	return false
}

// postComponent make http request with post method
func postComponent(component *sppv1.ComponentOption, base_url string) bool {
	url := base_url + "/components"
	data := &sppcommon.JsonData{"name": component.Name, "core": component.Core, "type": component.Type}
	return data.Request("POST", url)
}

func putPort(name string, base_url string, action string, dir string, port *sppv1.PortOption) bool {
	url := base_url + "/components/" + name + "/ports"
	data := &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port}
	if (port.Vlan.Operation == "add") || (port.Vlan.Operation == "del") || (port.Vlan.Operation == "none") {
		vlan := sppcommon.JsonData{"operation": port.Vlan.Operation, "id": port.Vlan.Id, "pcp": port.Vlan.Pcp}
		data = &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": vlan}
	}
	return data.Request("PUT", url)
}

//func (res *SppVfResponse) checkClassifierTableChanged(action string, ct []sppv1.ClassifierTableOption) []*JsonData{
func CheckClassifierTableChanged(res *sppv1.SppVfResponse, action string, ct []sppv1.ClassifierTableOption) []*sppcommon.JsonData {
	old_ct := []*sppcommon.JsonData{}
	new_ct := []*sppcommon.JsonData{}
	result := []*sppcommon.JsonData{}

	for _, ct := range res.ClassifierTable {
		data := &sppcommon.JsonData{"action": action, "type": ct.Type, "mac_address": ct.Value, "port": ct.Port}
		if ct.Type == "vlan" {
			tmp := strings.Split(ct.Value, "/")
			vlan, _ := strconv.Atoi(tmp[0])
			value := tmp[1]
			data = &sppcommon.JsonData{"action": action, "type": ct.Type, "mac_address": value, "port": ct.Port, "vlan": vlan}
		}
		old_ct = append(old_ct, data)
	}
	for _, ct := range ct {
		data := &sppcommon.JsonData{"action": action, "type": ct.Type, "mac_address": ct.Value, "port": ct.Port}
		if ct.Type == "vlan" {
			data = &sppcommon.JsonData{"action": action, "type": ct.Type, "mac_address": ct.Value, "port": ct.Port, "vlan": ct.Vlan}
		}
		new_ct = append(new_ct, data)
	}

	if action == "del" {
		for _, ct := range sppcommon.CompareDifference(old_ct, new_ct) {
			result = append(result, ct)
		}
	} else {
		for _, ct := range sppcommon.CompareDifference(new_ct, old_ct) {
			result = append(result, ct)
		}
	}

	return result
}

func CheckPortChanged(res *sppv1.ComponentResponse, action string, dir string, ports []sppv1.PortOption) []*sppcommon.JsonData {
	old_port := []*sppcommon.JsonData{}
	new_port := []*sppcommon.JsonData{}
	result := []*sppcommon.JsonData{}

	res_old_ports := res.RxPort
	if dir == "tx" {
		res_old_ports = res.TxPort
	}
	for _, port := range res_old_ports {
		data := &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": port.Vlan}
		if port.Vlan.Operation == "none" {
			vlan := sppcommon.JsonData{"operation": "none", "id": 0, "pcp": 0}
			data = &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": vlan}
		} else {
			id := port.Vlan.Id
			pcp := port.Vlan.Pcp
			//id, _:= strconv.Atoi(port.Vlan.Id)
			//pcp, _:= strconv.Atoi(port.Vlan.Pcp)
			vlan := sppcommon.JsonData{"operation": port.Vlan.Operation, "id": id, "pcp": pcp}
			data = &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": vlan}
		}
		old_port = append(old_port, data)
	}
	for _, port := range ports {
		data := &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": port.Vlan}
		if port.Vlan.Operation == "" {
			vlan := sppcommon.JsonData{"operation": "none", "id": 0, "pcp": 0}
			data = &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": vlan}
		} else {
			id := port.Vlan.Id
			pcp := port.Vlan.Pcp
			//id, _:= strconv.Atoi(port.Vlan.Id)
			//pcp, _:= strconv.Atoi(port.Vlan.Pcp)
			vlan := sppcommon.JsonData{"operation": port.Vlan.Operation, "id": id, "pcp": pcp}
			data = &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": vlan}
		}
		new_port = append(new_port, data)
	}

	if action == "detach" {
		for _, port := range sppcommon.CompareDifference(old_port, new_port) {
			result = append(result, port)
		}
	} else {
		for _, port := range sppcommon.CompareDifference(new_port, old_port) {
			result = append(result, port)
		}
	}

	return result
}

//func (res *SppVfResponse) checkClassifierTableHasPort(action string, port *JsonData) []*JsonData {
func CheckClassifierTableHasPort(res *sppv1.SppVfResponse, action string, port *sppcommon.JsonData) []*sppcommon.JsonData {
	tmp, _ := json.Marshal(port)
	port_json := &sppv1.PortResponse{}
	json.Unmarshal(tmp, port_json)
	result := []*sppcommon.JsonData{}
	for _, ct := range res.ClassifierTable {
		if port_json.Port == ct.Port {
			data := &sppcommon.JsonData{"action": action, "type": ct.Type, "mac_address": ct.Value, "port": ct.Port}
			if ct.Type == "vlan" {
				tmp := strings.Split(ct.Value, "/")
				vlan, _ := strconv.Atoi(tmp[0])
				value := tmp[1]
				data = &sppcommon.JsonData{"action": action, "type": ct.Type, "mac_address": value, "port": ct.Port, "vlan": vlan}
			}
			result = append(result, data)
		}
	}

	return result
}

func CheckComponentHasPort(res *sppv1.SppVfResponse, ct *sppcommon.JsonData) bool {
	tmp, _ := json.Marshal(ct)
	ct_json := &sppv1.ClassifierTableResponse{}
	json.Unmarshal(tmp, ct_json)
	for _, com := range res.Components {
		for _, rx := range com.RxPort {
			if ct_json.Port == rx.Port {
				return true
			}
		}
		for _, tx := range com.TxPort {
			if ct_json.Port == tx.Port {
				return true
			}
		}
	}

	return false
}

//func (res *SppVfResponse) checkComponentsChanged(action string, coms []sppv1.ComponentOption) []*JsonData{
func CheckComponentsChanged(res *sppv1.SppVfResponse, action string, coms []sppv1.ComponentOption) []*sppcommon.JsonData {
	old_com := []*sppcommon.JsonData{}
	new_com := []*sppcommon.JsonData{}
	result := []*sppcommon.JsonData{}

	for _, com := range res.Components {
		data := &sppcommon.JsonData{"name": com.Name, "core": com.Core, "type": com.Type}
		old_com = append(old_com, data)
	}
	for _, com := range coms {
		data := &sppcommon.JsonData{"name": com.Name, "core": com.Core, "type": com.Type}
		new_com = append(new_com, data)
	}

	if action == "del" {
		for _, com := range sppcommon.CompareDifference(old_com, new_com) {
			result = append(result, com)
		}
	} else {
		for _, com := range sppcommon.CompareDifference(new_com, old_com) {
			result = append(result, com)
		}
	}

	return result
}

func CheckComponentsAdded(res *sppv1.SppVfResponse, coms []sppv1.ComponentOption) []sppv1.ComponentOption {
	old_com := []*sppcommon.JsonData{}
	new_com := []*sppcommon.JsonData{}
	result := []sppv1.ComponentOption{}

	for _, com := range res.Components {
		data := &sppcommon.JsonData{"name": com.Name, "core": com.Core, "type": com.Type}
		old_com = append(old_com, data)
	}
	for _, com := range coms {
		data := &sppcommon.JsonData{"name": com.Name, "core": com.Core, "type": com.Type}
		new_com = append(new_com, data)
	}

	for _, com := range sppcommon.CompareDifference(new_com, old_com) {
		tmp, _ := json.Marshal(com)
		com_json := &sppv1.ComponentResponse{}
		json.Unmarshal(tmp, com_json)
		for _, com_v1 := range coms {
			if com_v1.Name == com_json.Name {
				result = append(result, com_v1)
				break
			}
		}

	}

	return result
}

func FindDeletedPorts(res *sppv1.SppVfResponse, component *sppcommon.JsonData) (string, []*sppcommon.JsonData) {
	//func (res *SppVfResponse) FindDeletedPorts(component *JsonData) (string, []*JsonData) {
	tmp, _ := json.Marshal(component)
	com_json := &sppv1.ComponentResponse{}
	json.Unmarshal(tmp, com_json)
	result := []*sppcommon.JsonData{}

	for _, com := range res.Components {
		if com_json.Name == com.Name {
			for _, port := range com.RxPort {
				data := &sppcommon.JsonData{"action": "detach", "dir": "rx", "port": port.Port, "vlan": port.Vlan}
				if port.Vlan.Operation == "none" {
					vlan := sppcommon.JsonData{"operation": "none", "id": 0, "pcp": 0}
					data = &sppcommon.JsonData{"action": "detach", "dir": "rx", "port": port.Port, "vlan": vlan}
				} else {
					id := port.Vlan.Id
					pcp := port.Vlan.Pcp
					vlan := sppcommon.JsonData{"operation": "del", "id": id, "pcp": pcp}
					data = &sppcommon.JsonData{"action": "detach", "dir": "rx", "port": port.Port, "vlan": vlan}
				}
				result = append(result, data)
			}
			for _, port := range com.TxPort {
				data := &sppcommon.JsonData{"action": "detach", "dir": "tx", "port": port.Port, "vlan": port.Vlan}
				if port.Vlan.Operation == "none" {
					vlan := sppcommon.JsonData{"operation": "none", "id": 0, "pcp": 0}
					data = &sppcommon.JsonData{"action": "detach", "dir": "tx", "port": port.Port, "vlan": vlan}
				} else {
					id := port.Vlan.Id
					pcp := port.Vlan.Pcp
					vlan := sppcommon.JsonData{"operation": "del", "id": id, "pcp": pcp}
					data = &sppcommon.JsonData{"action": "detach", "dir": "tx", "port": port.Port, "vlan": vlan}
				}
				result = append(result, data)
			}
			break
		}
	}

	return com_json.Name, result
}

func FindAddPorts(res *sppv1.SppVfResponse, component *sppcommon.JsonData) (string, []*sppcommon.JsonData) {
	tmp, _ := json.Marshal(component)
	com_json := &sppv1.ComponentResponse{}
	json.Unmarshal(tmp, com_json)
	result := []*sppcommon.JsonData{}

	for _, com := range res.Components {
		if com_json.Name == com.Name {
			for _, port := range com.RxPort {
				data := &sppcommon.JsonData{"action": "detach", "dir": "rx", "port": port.Port, "vlan": port.Vlan}
				if port.Vlan.Operation == "none" {
					vlan := sppcommon.JsonData{"operation": "none", "id": 0, "pcp": 0}
					data = &sppcommon.JsonData{"action": "detach", "dir": "rx", "port": port.Port, "vlan": vlan}
				} else {
					id := port.Vlan.Id
					pcp := port.Vlan.Pcp
					vlan := sppcommon.JsonData{"operation": "del", "id": id, "pcp": pcp}
					data = &sppcommon.JsonData{"action": "detach", "dir": "rx", "port": port.Port, "vlan": vlan}
				}
				result = append(result, data)
			}
			for _, port := range com.TxPort {
				data := &sppcommon.JsonData{"action": "detach", "dir": "tx", "port": port.Port, "vlan": port.Vlan}
				if port.Vlan.Operation == "none" {
					vlan := sppcommon.JsonData{"operation": "none", "id": 0, "pcp": 0}
					data = &sppcommon.JsonData{"action": "detach", "dir": "tx", "port": port.Port, "vlan": vlan}
				} else {
					id := port.Vlan.Id
					pcp := port.Vlan.Pcp
					vlan := sppcommon.JsonData{"operation": "del", "id": id, "pcp": pcp}
					data = &sppcommon.JsonData{"action": "detach", "dir": "tx", "port": port.Port, "vlan": vlan}
				}
				result = append(result, data)
			}
			break
		}
	}

	return com_json.Name, result
}

func InitNewPort(port *sppv1.PortOption, name string, base_url string, action string, dir string) bool {
	url := base_url + "/" + name + "/ports"
	data := &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port}
	if (port.Vlan.Operation == "add") || (port.Vlan.Operation == "del") || (port.Vlan.Operation == "none") {
		vlan := sppcommon.JsonData{"operation": port.Vlan.Operation, "id": port.Vlan.Id, "pcp": port.Vlan.Pcp}
		data = &sppcommon.JsonData{"action": action, "dir": dir, "port": port.Port, "vlan": vlan}
	}
	return data.Request("PUT", url)
}

func InitNewComponent(component *sppv1.ComponentOption, base_url string) bool {
	url := base_url + "/components"
	component_data := &sppcommon.JsonData{"name": component.Name, "core": component.Core, "type": component.Type}
	if component_data.Request("POST", url) {
		for _, rx := range component.RxPort {
			if !InitNewPort(&rx, component.Name, url, "attach", "rx") {
				fmt.Println("InitNewPort Rx Faild :", rx)
			}
		}
		for _, tx := range component.TxPort {
			if !InitNewPort(&tx, component.Name, url, "attach", "tx") {
				fmt.Println("InitNewPort Tx Faild :", tx)
			}
		}
		return true
	} else {
		fmt.Println("InitNewComponent Faild :", component)
		return false
	}
}

func InitNewClassifierTable(ct *sppv1.ClassifierTableOption, url string, action string) bool {
	data := &sppcommon.JsonData{"action": action, "type": ct.Type, "port": ct.Port, "mac_address": ct.Value}
	if ct.Vlan != 0 {
		data = &sppcommon.JsonData{"action": action, "type": ct.Type, "port": ct.Port, "mac_address": ct.Value, "vlan": ct.Vlan}
	}
	return data.Request("PUT", url+"/classifier_table")
}
