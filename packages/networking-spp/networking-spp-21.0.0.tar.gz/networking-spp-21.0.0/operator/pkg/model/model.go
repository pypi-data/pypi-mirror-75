package model

import (
	"fmt"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/intstr"
	sppv1 "opendev.org/x/networking-spp/operator/pkg/apis/spp/v1"
	sppcommon "opendev.org/x/networking-spp/operator/pkg/model/common"
	sppnfv "opendev.org/x/networking-spp/operator/pkg/model/nfv"
	sppvf "opendev.org/x/networking-spp/operator/pkg/model/vf"
	"strconv"
	"strings"
	"time"
)

type Spp struct {
	V1 *sppv1.Spp
}

/*
Spp common functions
*/

func (spp *Spp) BaseUrl() string {
	return "http://" + spp.V1.Status.ServiceVip + ":" + strconv.Itoa(sppcommon.CTL_CLI_PORT_NUM)
}

// Delete calles SPP API to tell ctl the pod is deleted
func (spp *Spp) Delete(kind string, secId string) bool {
	url := spp.BaseUrl() + "/v1/"

	if kind == "vf" {
		url = url + "vfs/" + secId
	} else if kind == "mirror" {
		url = url + "mirrors/" + secId
	} else if kind == "nfv" {
		url = url + "nfvs/" + secId
	} else if kind == "pcap" {
		url = url + "pcaps/" + secId
	} else {
	}

	return sppcommon.HttpDeleteRequest(url)
	//return true
}

/*
Spp Ctl
*/
// NewCtl makes a ctl pod and service using CR from yaml
func (spp *Spp) NewCtl() (*corev1.Pod, *corev1.Service) {
	label := sppcommon.MakeLabel(spp.V1.Name, spp.V1.Spec.Ctl.Name)
	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)

	/* make a pod for ctl */
	CtlPod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, spp.V1.Spec.Ctl.Name, "pod"),
			Namespace: spp.V1.Namespace,
			Labels:    label,
		},
		Spec: corev1.PodSpec{
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    spp.V1.Spec.Ctl.Name,
					Image:   spp.V1.Spec.Ctl.Image,
					Command: []string{"/root/start-spp-ctl.sh"},
					Ports: []corev1.ContainerPort{
						{
							Name:          "primary",
							ContainerPort: sppcommon.CTL_PRI_PORT_NUM,
							Protocol:      "TCP",
						},
						{
							Name:          "secondary",
							ContainerPort: sppcommon.CTL_SEC_PORT_NUM,
							Protocol:      "TCP",
						},
						{
							Name:          "cli",
							ContainerPort: sppcommon.CTL_CLI_PORT_NUM,
							Protocol:      "TCP",
						},
					},
				},
			},
		},
	}

	/* make a service for ctl */
	CtlService := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, spp.V1.Spec.Ctl.Name, "service"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.ServiceSpec{
			Selector: label,
			Ports: []corev1.ServicePort{
				{
					Name:       "primary",
					Port:       sppcommon.CTL_PRI_PORT_NUM,
					TargetPort: intstr.FromInt(sppcommon.CTL_PRI_PORT_NUM),
					Protocol:   "TCP",
				},
				{
					Name:       "secondary",
					Port:       sppcommon.CTL_SEC_PORT_NUM,
					TargetPort: intstr.FromInt(sppcommon.CTL_SEC_PORT_NUM),
					Protocol:   "TCP",
				},
				{
					Name:       "cli",
					Port:       sppcommon.CTL_CLI_PORT_NUM,
					TargetPort: intstr.FromInt(sppcommon.CTL_CLI_PORT_NUM),
					Protocol:   "TCP",
				},
			},
		},
	}

	return CtlPod, CtlService
}

/*
Spp Primary
*/
// NewPrimary makes a primary pod using CR from yaml
func (spp *Spp) NewPrimary() *corev1.Pod {
	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)
	args := "spp_primary -l " + spp.V1.Spec.Primary.Eal.Lcores + " -n 4 --socket-mem " + spp.V1.Spec.Primary.Eal.SocketMem + " --huge-dir /dev/hugepages --base-virtaddr 0x100000000 --proc-type primary"
	if spp.V1.Spec.Primary.Eal.Vdevs != nil {
		args += " --vdev "
		for _, value := range spp.V1.Spec.Primary.Eal.Vdevs {
			args += strings.Join(value, ",")
		}
	}
	args += " -- -p " + spp.V1.Spec.Primary.PortMask + " -n 10 -s " + spp.V1.Status.ServiceVip + ":" + strconv.Itoa(sppcommon.CTL_PRI_PORT_NUM)

	privileged := true
	PrimaryPod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, spp.V1.Spec.Primary.Name, "pod"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.PodSpec{
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    spp.V1.Spec.Primary.Name,
					Image:   spp.V1.Spec.Primary.Image,
					Command: []string{"/bin/bash", "-c"},
					SecurityContext: &corev1.SecurityContext{
						Privileged: &privileged,
					},
					Args: []string{args},
					Resources: corev1.ResourceRequirements{
						Limits: sppcommon.ResourcesForHugePage("1Gi"),
					},
					VolumeMounts: []corev1.VolumeMount{
						sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
						sppcommon.MakeVolumeMount("dpdk", "/var/run"),
						sppcommon.MakeVolumeMount("nic", "/sys/devices"),
					},
				},
			},
			Volumes: []corev1.Volume{
				sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
				sppcommon.MakeVolume("dpdk", "/var/run"),
				sppcommon.MakeVolume("nic", "/sys/devices"),
			},
		},
	}

	return PrimaryPod
}

/*
Spp running check funcionts
*/
// get processes using REST API
func (spp *Spp) GetProcesses() ([]sppv1.SppProcessResponse, bool) {
	url := spp.BaseUrl() + "/v1/processes"
	// get response using REST API
	spp_processes_res := []sppv1.SppProcessResponse{}
	status := sppcommon.HttpGetRequestAsJson(url, &spp_processes_res)
	return spp_processes_res, status
}

// check if procces(ctl or primary) is runnning using REST API
func (spp *Spp) CheckRunning(kind string, retry int) bool {
	if spp.V1.Status.ServiceVip != "" {
		spp_processes_res, status := spp.GetProcesses()

		for count := 0; count < retry; count++ {
			if kind == "ctl" {
				if status {
					fmt.Println("Confirmed Ctl is Running")
					return true
				} else {
					fmt.Printf("Retrying to check ctl status: retry_times=%v, status=%v, response=%v\n", count, status, spp_processes_res)
					time.Sleep(10 * time.Second)
					spp_processes_res, status = spp.GetProcesses()
				}
			} else if kind == "primary" {
				if status && len(spp_processes_res) > 0 {
					if spp_processes_res[0].Type == "primary" {
						fmt.Println("Confirmed Primary is Running")
						return true
					}
				} else {
					fmt.Printf("Retrying to check primary status: retry_times=%v, status=%v, response=%v\n", count, status, spp_processes_res)
					time.Sleep(10 * time.Second)
					spp_processes_res, status = spp.GetProcesses()
				}
			} else {
				fmt.Printf("Unexpected kind of %v has been detected. The kind must be ctl or primary\n", kind)
				return false
			}
		}
		fmt.Println("Check Running Retry Timeout", kind)
		return false
	} else {
		return false
	}
}

// check if all nfvs are runnning using REST API
func (spp *Spp) CheckNfvsRunning() bool {
	base_url := spp.BaseUrl() + "/v1/nfvs/"

	for _, nfv := range spp.V1.Spec.Nfvs {
		// get secId and make url
		_, secId := sppcommon.GetSecId(nfv.Name)
		url := base_url + secId

		// get response using REST API
		spp_nfv_res := sppv1.SppNfvResponse{}
		sppcommon.HttpGetRequestAsJson(url, &spp_nfv_res)

		if spp_nfv_res.Status != "running" {
			return false
		}
	}
	return true
}

func (spp *Spp) CheckVfsRunning() bool {
	base_url := spp.BaseUrl() + "/v1/vfs/"

	for _, vf := range spp.V1.Spec.Vfs {
		// get secId and make url
		_, secId := sppcommon.GetSecId(vf.Name)
		url := base_url + secId

		// get response using REST API
		spp_vf_res := sppv1.SppVfResponse{}
		sppcommon.HttpGetRequestAsJson(url, &spp_vf_res)

		if strconv.Itoa(spp_vf_res.ClientId) != secId {
			return false
		}
	}
	return true
}

func (spp *Spp) CheckMirrorsRunning() bool {
	base_url := spp.BaseUrl() + "/v1/mirrors/"

	for _, mirror := range spp.V1.Spec.Mirrors {
		// get secId and make url
		_, secId := sppcommon.GetSecId(mirror.Name)
		url := base_url + secId

		// get response using REST API
		spp_mirror_res := sppv1.SppVfResponse{}
		sppcommon.HttpGetRequestAsJson(url, &spp_mirror_res)

		if strconv.Itoa(spp_mirror_res.ClientId) != secId {
			return false
		}
	}
	return true
}

func (spp *Spp) CheckReady() bool {
	return (spp.CheckNfvsRunning() && spp.CheckVfsRunning() && spp.CheckMirrorsRunning())
}

/*
Spp Nfv
*/
// NewNfv makes a nfv pod from cr nfvs using index
func (spp *Spp) NewNfv(index int) *corev1.Pod {
	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)
	nfv := spp.V1.Spec.Nfvs[index]
	name, secId := sppcommon.GetSecId(nfv.Name)
	privileged := true
	args := "spp_nfv -l " + nfv.Eal.Lcores + " -n 4 --socket-mem " + nfv.Eal.SocketMem + " --proc-type secondary  -- -n " + secId + " -s " + spp.V1.Status.ServiceVip + ":" + strconv.Itoa(sppcommon.CTL_SEC_PORT_NUM)

	if nfv.Vhost == "client" {
		args = args + " --vhost-client"
	}

	nfv_pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, name+"-"+secId, "pod"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.PodSpec{
			HostPID:      true,
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    "nfv",
					Image:   nfv.Image,
					Command: []string{"/bin/bash", "-c"},
					SecurityContext: &corev1.SecurityContext{
						Privileged: &privileged,
					},
					Args: []string{args},
					Resources: corev1.ResourceRequirements{
						Limits: sppcommon.ResourcesForHugePage("1Gi"),
					},
					VolumeMounts: []corev1.VolumeMount{
						sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
						sppcommon.MakeVolumeMount("dpdk", "/var/run"),
						sppcommon.MakeVolumeMount("tmp", "/tmp"),
						sppcommon.MakeVolumeMount("nic", "/sys/devices"),
					},
				},
			},
			Volumes: []corev1.Volume{
				sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
				sppcommon.MakeVolume("dpdk", "/var/run"),
				sppcommon.MakeVolume("tmp", "/tmp"),
				sppcommon.MakeVolume("nic", "/sys/devices"),
			},
		},
	}
	return nfv_pod
}

func (spp *Spp) BeforeDeleteNfv(secId string) {
	url := spp.BaseUrl() + "/v1/nfvs/" + secId

	// get response using REST API
	spp_nfv_res := &sppv1.SppNfvResponse{}
	sppcommon.HttpGetRequestAsJson(url, spp_nfv_res)

	if sppnfv.CheckResourcesExist(spp_nfv_res) {
		// make the nfv forward to stop
		spp.MakeNfvForward(secId, "stop")
		// delete patches
		sppcommon.HttpDeleteRequest(url + "/patches")

		// delete all resources
		for _, resource := range spp_nfv_res.Resources {
			if strings.Contains(resource, "vhost") || strings.Contains(resource, "ring") {
				fmt.Println("Resource Deleted", resource)
				sppnfv.PutResources(resource, url, "del")
			}
		}
	}

}

// make nfv forward
func (spp *Spp) MakeNfvForward(secId string, action string) bool {
	url := spp.BaseUrl() + "/v1/nfvs/" + secId + "/forward"
	data := &sppcommon.JsonData{"action": action}

	// flag of res
	successful := false
	if sppcommon.HttpRequest("PUT", url, data) {
		successful = true
	}
	fmt.Println("nfv forward secId :", secId, action, successful)
	return successful
}

func (spp *Spp) ReconcileNfv(secId string, nfv *sppv1.SppNfv) *sppv1.SppNfvResponse {
	url := spp.BaseUrl() + "/v1/nfvs/" + secId

	// get response using REST API
	spp_nfv_res := &sppv1.SppNfvResponse{}
	sppcommon.HttpGetRequestAsJson(url, spp_nfv_res)
	fmt.Println("=============================== NFV Reconcile ==================================")
	fmt.Println("Spp Name: ", spp.V1.Name)
	fmt.Println("secId: ", secId)
	fmt.Println("Status : ", spp_nfv_res.Status)

	//if spp_nfv_res.checkResourcesExist(){
	if sppnfv.CheckResourcesExist(spp_nfv_res) {
		deleted_resources, added_resources := sppnfv.CheckResourcesChanged(spp_nfv_res, nfv.Resources)
		patches_changed := sppnfv.CheckPatchesChanged(spp_nfv_res, nfv.Patches)

		fmt.Println("Patches Changed: ", patches_changed)
		fmt.Println("Resources Deleted:", deleted_resources)
		fmt.Println("Resources Added:", added_resources)

		if patches_changed {
			// make the nfv forward to stop
			spp.MakeNfvForward(secId, "stop")
			// delete patches
			sppcommon.HttpDeleteRequest(url + "/patches")
		}

		for _, resource := range deleted_resources {
			fmt.Println("Resource Deleted", resource)
			sppnfv.PutResources(resource, url, "del")
		}

		for _, resource := range added_resources {
			fmt.Println("Resource Added", resource)
			sppnfv.PutResources(resource, url, "add")
		}

		if patches_changed {
			// add patches from CR
			for _, patch := range nfv.Patches {
				sppnfv.PutPatches(patch, url)
			}
			// make the nfv foward to start
			spp.MakeNfvForward(secId, "start")
		}

	} else {
		// init resources and patches
		fmt.Println("Init resources and patches")
		for _, resource := range nfv.Resources {
			sppnfv.PutResources(resource, url, "add")
		}
		for _, patch := range nfv.Patches {
			sppnfv.PutPatches(patch, url)
		}
		// make the nfv forward to start
		spp.MakeNfvForward(secId, "start")
	}

	//spp_nfv_res_print := &sppv1.SppNfvResponse{}
	sppcommon.HttpGetRequestAsJson(url, spp_nfv_res)

	return spp_nfv_res
}

// GetSecIdsFromCR makes secIds from index of cr.nfvs
func (spp *Spp) GetNfvSecIdsFromCR() []string {
	secIds := []string{}
	for i, _ := range spp.V1.Spec.Nfvs {
		_, secId := sppcommon.GetSecId(spp.V1.Spec.Nfvs[i].Name)
		secIds = append(secIds, secId)
	}
	return secIds
}

// OldNfvs make secId which does not exist in cr by comparing cr and NfvSecIdsIndexMap
func (spp *Spp) OldNfvs() []string {
	removed_pods := []string{}
	secIds := spp.GetNfvSecIdsFromCR()
	//for secId, _ := range spp.NfvPods {
	for secId, _ := range spp.V1.Status.Nfvs.Pods {
		if sppcommon.StringInSlice(secId, secIds) {
			removed_pods = append(removed_pods, secId)
		}
	}

	return removed_pods
}

/*
spp vf and mirror
*/

// New makes vf pod
func (spp *Spp) NewVf(index int) *corev1.Pod {
	command := "spp_vf"

	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)
	vf := spp.V1.Spec.Vfs[index]
	name, secId := sppcommon.GetSecId(vf.Name)
	privileged := true
	args := command + " -l " + vf.Eal.Lcores + " -n 4 " + vf.Eal.SocketMem + " --proc-type secondary  -- --client-id " + secId + " -s " + spp.V1.Status.ServiceVip + ":" + strconv.Itoa(sppcommon.CTL_SEC_PORT_NUM) + " --vhost-client"
	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, name+"-"+secId, "pod"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.PodSpec{
			//RestartPolicy: "Never",
			HostPID:      true,
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    "vf",
					Image:   vf.Image,
					Command: []string{"/bin/bash", "-c"},
					SecurityContext: &corev1.SecurityContext{
						Privileged: &privileged,
					},
					Args: []string{args},
					Resources: corev1.ResourceRequirements{
						Limits: sppcommon.ResourcesForHugePage("1Gi"),
					},
					VolumeMounts: []corev1.VolumeMount{
						sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
						sppcommon.MakeVolumeMount("dpdk", "/var/run"),
						sppcommon.MakeVolumeMount("tmp", "/tmp"),
						sppcommon.MakeVolumeMount("nic", "/sys/devices"),
						sppcommon.MakeVolumeMount("lib", "/lib/sys/systemd-coredump"),
					},
				},
			},
			Volumes: []corev1.Volume{
				sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
				sppcommon.MakeVolume("dpdk", "/var/run"),
				sppcommon.MakeVolume("tmp", "/tmp"),
				sppcommon.MakeVolume("nic", "/sys/devices"),
				sppcommon.MakeVolume("lib", "/lib/sys/systemd-coredump"),
			},
		},
	}

	return pod
}

// New makes mirror pod
func (spp *Spp) NewMirror(index int) *corev1.Pod {
	command := "spp_mirror"

	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)
	vf := spp.V1.Spec.Mirrors[index]
	name, secId := sppcommon.GetSecId(vf.Name)
	privileged := true
	args := command + " -l " + vf.Eal.Lcores + " -n 4 " + vf.Eal.SocketMem + " --proc-type secondary  -- --client-id " + secId + " -s " + spp.V1.Status.ServiceVip + ":" + strconv.Itoa(sppcommon.CTL_SEC_PORT_NUM) + " --vhost-client"
	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, name+"-"+secId, "pod"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.PodSpec{
			//RestartPolicy: "Never",
			HostPID:      true,
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    "vf",
					Image:   vf.Image,
					Command: []string{"/bin/bash", "-c"},
					SecurityContext: &corev1.SecurityContext{
						Privileged: &privileged,
					},
					Args: []string{args},
					Resources: corev1.ResourceRequirements{
						Limits: sppcommon.ResourcesForHugePage("1Gi"),
					},
					VolumeMounts: []corev1.VolumeMount{
						sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
						sppcommon.MakeVolumeMount("dpdk", "/var/run"),
						sppcommon.MakeVolumeMount("tmp", "/tmp"),
						sppcommon.MakeVolumeMount("nic", "/sys/devices"),
						sppcommon.MakeVolumeMount("lib", "/lib/sys/systemd-coredump"),
					},
				},
			},
			Volumes: []corev1.Volume{
				sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
				sppcommon.MakeVolume("dpdk", "/var/run"),
				sppcommon.MakeVolume("tmp", "/tmp"),
				sppcommon.MakeVolume("nic", "/sys/devices"),
				sppcommon.MakeVolume("lib", "/lib/sys/systemd-coredump"),
			},
		},
	}

	return pod
}

//func (spp *Spp) Reconcile(secId string, vf *sppv1.SppVf) {
func (spp *Spp) Reconcile(secId string, kind string, Components []sppv1.ComponentOption, ClassifierTable []sppv1.ClassifierTableOption) *sppv1.SppVfResponse {

	url := spp.BaseUrl() + "/v1/"

	if kind == "vf" {
		url = url + "vfs/" + secId
	} else {
		url = url + "mirrors/" + secId
	}

	// get response using REST API
	res := &sppv1.SppVfResponse{}
	sppcommon.HttpGetRequestAsJson(url, res)
	fmt.Println("=============================== Reconcile ==================================")
	fmt.Println("Spp Name: ", spp.V1.Name)
	fmt.Println("Kind:", kind)
	fmt.Println("secId: ", secId)
	fmt.Println("URL:", url)
	fmt.Println("CR Components: ", Components)
	fmt.Println("CR ClassifierTable: ", ClassifierTable)
	fmt.Println("Response from REST API: ", res)

	fmt.Println("**********************Reconcile Components Delete Phase*******************************")

	// Delete phase ClassifierTable which CR does not have
	for _, ct := range sppvf.CheckClassifierTableChanged(res, "del", ClassifierTable) {
		if ct.Request("PUT", url+"/classifier_table") {
			fmt.Println("Deleted ClassifierTable :", ct)
		}
		// get response using REST API again
		sppcommon.HttpGetRequestAsJson(url, res)
	}

	// Delete phase the RxPort and TxPort which new CR components do not have
	for _, com := range Components {
		for _, res_com := range res.Components {
			// only compare coms which have same name, core and type
			if (com.Name == res_com.Name) && (com.Core == res_com.Core) && (com.Type == res_com.Type) {
				fmt.Println("Reconcile Ports of Component :", com.Name)
				// RX
				for _, port := range sppvf.CheckPortChanged(&res_com, "detach", "rx", com.RxPort) {
					for _, ct := range sppvf.CheckClassifierTableHasPort(res, "del", port) {
						if ct.Request("PUT", url+"/classifier_table") {
							fmt.Println("Deleted ClassifierTable which has deleted RX ports :", ct)
						}
						// get response using REST API again
						sppcommon.HttpGetRequestAsJson(url, res)
					}
					if port.Request("PUT", url+"/components/"+com.Name+"/ports") {
						fmt.Println("Deleted RX Port :", port)
					}
				}
				// TX
				for _, port := range sppvf.CheckPortChanged(&res_com, "detach", "tx", com.TxPort) {
					for _, ct := range sppvf.CheckClassifierTableHasPort(res, "del", port) {
						if ct.Request("PUT", url+"/classifier_table") {
							fmt.Println("Deleted ClassifierTable which has deleted TX ports: ", ct)
						}
						// get response using REST API again
						sppcommon.HttpGetRequestAsJson(url, res)
					}
					if port.Request("PUT", url+"/components/"+com.Name+"/ports") {
						fmt.Println("Deleted TX Port :", port)
					}
				}
			}
		}
	}

	// get response using REST API again
	sppcommon.HttpGetRequestAsJson(url, res)

	// Delete phase the Components which new CR does not have
	for _, com := range sppvf.CheckComponentsChanged(res, "del", Components) {
		com_name, ports := sppvf.FindDeletedPorts(res, com)
		fmt.Println("Deleted Component :", com_name)
		for _, port := range ports {
			for _, ct := range sppvf.CheckClassifierTableHasPort(res, "del", port) {
				if ct.Request("PUT", url+"/classifier_table") {
					fmt.Println("Deleted ClassifierTable which has deleted RX/TX port: ", ct)
				}
			}
			if port.Request("PUT", url+"/components/"+com_name+"/ports") {
				fmt.Println("Deleted Rx/Tx Port which deleted Components have: ", port)
			}
		}
		// get response using REST API again
		sppcommon.HttpGetRequestAsJson(url, res)

		//
		if sppcommon.HttpDeleteRequest(url + "/components/" + com_name) {
			fmt.Println("Deleted Component :", com_name)
		}
	}

	// get response using REST API again
	sppcommon.HttpGetRequestAsJson(url, res)

	// Add phase new Components
	fmt.Println("**********************Reconcile Components Add Phase*******************************")
	//for _, com := range spp_vf_res.checkComponentsChanged("add", vf.Components){
	for _, component := range sppvf.CheckComponentsAdded(res, Components) {
		if sppvf.InitNewComponent(&component, url) {
			fmt.Println("Added New Component :", component)
		}
		// get response using REST API again
		sppcommon.HttpGetRequestAsJson(url, res)
	}

	// get response using REST API again
	sppcommon.HttpGetRequestAsJson(url, res)
	// Add phase RxPort, TxPort which new components have
	for _, com := range Components {
		for _, res_com := range res.Components {
			// only compare coms which have same name, core and type
			if (com.Name == res_com.Name) && (com.Core == res_com.Core) && (com.Type == res_com.Type) {
				fmt.Println("Reconcile Ports of Component :", com.Name)
				// RX
				for _, port := range sppvf.CheckPortChanged(&res_com, "attach", "rx", com.RxPort) {
					if port.Request("PUT", url+"/components/"+com.Name+"/ports") {
						fmt.Println("Added Rx port", port)
					}
				}
				// TX
				for _, port := range sppvf.CheckPortChanged(&res_com, "attach", "tx", com.TxPort) {
					if port.Request("PUT", url+"/components/"+com.Name+"/ports") {
						fmt.Println("Added TX port", port)
					}
				}
			}
			// get response using REST API again
			sppcommon.HttpGetRequestAsJson(url, res)
		}
	}

	// get response using REST API again
	sppcommon.HttpGetRequestAsJson(url, res)
	// Add phase ClassifierTable
	if sppvf.CheckComponentsExist(res) {
		for _, ct := range sppvf.CheckClassifierTableChanged(res, "add", ClassifierTable) {
			if sppvf.CheckComponentHasPort(res, ct) {
				if ct.Request("PUT", url+"/classifier_table") {
					fmt.Println("Added ClassifierTable :", ct)
				}
			} else {
				fmt.Println("The Port of Classifier table does not exist in any Components:", ct)
			}
			// get response using REST API again
			sppcommon.HttpGetRequestAsJson(url, res)
		}
	}

	sppcommon.HttpGetRequestAsJson(url, res)

	return res

}

func (spp *Spp) GetVfSecIdsFromCR() []string {
	secIds := []string{}
	for i, _ := range spp.V1.Spec.Vfs {
		_, secId := sppcommon.GetSecId(spp.V1.Spec.Vfs[i].Name)
		secIds = append(secIds, secId)
	}
	return secIds
}

func (spp *Spp) GetMirrorSecIdsFromCR() []string {
	secIds := []string{}
	for i, _ := range spp.V1.Spec.Mirrors {
		_, secId := sppcommon.GetSecId(spp.V1.Spec.Mirrors[i].Name)
		secIds = append(secIds, secId)
	}
	return secIds
}

func (spp *Spp) Olds(kind string) []string {
	removed_pods := []string{}
	secIds := []string{}

	if kind == "vf" {
		secIds = spp.GetVfSecIdsFromCR()
		for secId, _ := range spp.V1.Status.Vfs.Pods {
			if sppcommon.StringInSlice(secId, secIds) {
				removed_pods = append(removed_pods, secId)
			}
		}
	} else {
		secIds = spp.GetMirrorSecIdsFromCR()
		for secId, _ := range spp.V1.Status.Mirrors.Pods {
			if sppcommon.StringInSlice(secId, secIds) {
				removed_pods = append(removed_pods, secId)
			}
		}
	}

	return removed_pods
}

/*
Spp PCAP
*/
// NewPcap makes a pcap pod from cr pcaps using index
func (spp *Spp) NewPcap(index int) *corev1.Pod {
	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)
	pcap := spp.V1.Spec.Pcaps[index]
	name, secId := sppcommon.GetSecId(pcap.Name)
	privileged := true
	args := "spp_pcap -l " + pcap.Eal.Lcores + " -n 4 --socket-mem " + pcap.Eal.SocketMem + " --proc-type secondary  -- --client-id " + secId + " -s " + spp.V1.Status.ServiceVip + ":" + strconv.Itoa(sppcommon.CTL_SEC_PORT_NUM) + " -c " + pcap.Port

	volumeMounts := []corev1.VolumeMount{
		sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
		sppcommon.MakeVolumeMount("dpdk", "/var/run"),
		sppcommon.MakeVolumeMount("tmp", "/tmp"),
		sppcommon.MakeVolumeMount("nic", "/sys/devices"),
	}
	volumes := []corev1.Volume{
		sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
		sppcommon.MakeVolume("dpdk", "/var/run"),
		sppcommon.MakeVolume("tmp", "/tmp"),
		sppcommon.MakeVolume("nic", "/sys/devices"),
	}

	if pcap.OutDir != "" {
		slice := strings.Split(pcap.OutDir, ":")
		if len(slice) > 1 {
			if slice[0] != "" {
				args += " --out-dir " + slice[0]
			}
			if slice[1] != "" {
				volumeMounts = []corev1.VolumeMount{
					sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
					sppcommon.MakeVolumeMount("dpdk", "/var/run"),
					sppcommon.MakeVolumeMount("tmp", "/tmp"),
					sppcommon.MakeVolumeMount("nic", "/sys/devices"),
					sppcommon.MakeVolumeMount("outdir", slice[0]),
				}
				volumes = []corev1.Volume{
					sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
					sppcommon.MakeVolume("dpdk", "/var/run"),
					sppcommon.MakeVolume("tmp", "/tmp"),
					sppcommon.MakeVolume("nic", "/sys/devices"),
					sppcommon.MakeVolume("outdir", slice[1]),
				}
			}
		} else {
			fmt.Println("Pcap out_dir option is invalid")
		}
	}
	if pcap.Fsize != 0 {
		args += " --fsize " + strconv.Itoa(pcap.Fsize)
	}

	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, name+"-"+secId, "pod"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.PodSpec{
			HostPID:      true,
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    "pcap",
					Image:   pcap.Image,
					Command: []string{"/bin/bash", "-c"},
					SecurityContext: &corev1.SecurityContext{
						Privileged: &privileged,
					},
					Args: []string{args},
					Resources: corev1.ResourceRequirements{
						Limits: sppcommon.ResourcesForHugePage("1Gi"),
					},
					VolumeMounts: volumeMounts,
				},
			},
			Volumes: volumes,
		},
	}
	return pod
}

func (spp *Spp) ReconcilePcap(secId string, pcap *sppv1.SppPcap) *sppv1.SppPcapResponse {
	url := spp.BaseUrl() + "/v1/pcaps/" + secId

	// get response using REST API
	res := &sppv1.SppPcapResponse{}
	sppcommon.HttpGetRequestAsJson(url, res)
	fmt.Println("=============================== PCAP Reconcile ==================================")
	fmt.Println("Spp Name: ", spp.V1.Name)
	fmt.Println("secId: ", secId)
	fmt.Println("Status : ", res.Status)
	fmt.Println("Status CR: ", pcap.Status)

	if (res.Status == "idle") && (pcap.Status == "running") {
		data := &sppcommon.JsonData{"action": "start"}
		if data.Request("PUT", url+"/capture") {
			fmt.Println("Make Pcap forward start")
		}
	} else if (res.Status == "running") && (pcap.Status != "running") {
		data := &sppcommon.JsonData{"action": "stop"}
		if data.Request("PUT", url+"/capture") {
			fmt.Println("Make Pcap forward stop")
		}
	} else {
		fmt.Println("Pcap status is same to CR")
	}

	sppcommon.HttpGetRequestAsJson(url, res)

	return res

}

// GetSecIdsFromCR makes secIds from index of cr.nfvs
func (spp *Spp) GetPcapSecIdsFromCR() []string {
	secIds := []string{}
	for i, _ := range spp.V1.Spec.Pcaps {
		_, secId := sppcommon.GetSecId(spp.V1.Spec.Pcaps[i].Name)
		secIds = append(secIds, secId)
	}
	return secIds
}

func (spp *Spp) OldPcaps() []string {
	removed_pods := []string{}
	secIds := spp.GetPcapSecIdsFromCR()
	for secId, _ := range spp.V1.Status.Pcaps.Pods {
		if sppcommon.StringInSlice(secId, secIds) {
			removed_pods = append(removed_pods, secId)
		}
	}

	return removed_pods
}

/*
Apps
*/
// make an app args by app's name
func (spp *Spp) makeAppArgs(index int) string {
	app := spp.V1.Spec.Apps[index]
	args := app.Command[0] + " -l " + app.Eal.Lcores + " -n 4 --socket-mem " + app.Eal.SocketMem + " --proc-type auto"
	vdev := ""
	for _, value := range app.Eal.Vdevs {
		vdev += " --vdev "
		vdev += strings.Join(value, ",")
	}
	args += vdev

	switch app.Name {
	case "testpmd":
		args += " --file-prefix testpmd -- --no-numa --tx-first && sleep 3600"
	case "l2fwd":
		args = "/root/dpdk/examples/l2fwd/x86_64-native-linuxapp-gcc/" + args
		args += " --file-prefix l2fwd -- -p 0x03"
	}
	return args
	//return "sleep 3600"
}

// make an app args by app's name
func (spp *Spp) makeAppArgsPipetest(index int) (string, string, bool) {
	app := spp.V1.Spec.Apps[index]
	slice := strings.Split(app.Name, ":")
	name := slice[0] + "-" + slice[1]

	/*
	   vhost

	       pipe_test --lcores 4,6 -n 4 --vdev virtio_user1,path=/tmp/sock1,server=1 --file-prefix=app1 --base-virtaddr 0x100000000 --single-file-segments -- virtio_user1

	       pipe_test -c 0x10 -n 4 --vdev virtio_user1,path=/tmp/sock1,server=1 --file-prefix=app1 --single-file-segments -- virtio_user1
	       pipe_test -c 0x20 -n 4 --vdev virtio_user2,path=/tmp/sock2,server=1 --file-prefix=app2 --single-file-segments -- --send virtio_user2

	   pipe
	       pipe_test -c 0x10 -n 4 --proc-type secondary --vdev net_pipe0,rx=ring:1,tx=ring:2 -- net_pipe0
	       pipe_test -c 0x20 -n 4 --proc-type secondary --vdev net_pipe1,rx=ring:3,tx=ring:4 -- --send net_pipe1
	*/

	hostPID := false
	args := app.Command[0] + " --lcores " + app.Eal.Lcores + " -n 4 "
	if app.Type == "vhost" {
		args += " --file-prefix=" + name + " --base-virtaddr 0x100000000 --single-file-segments"
	} else {
		args += " --proc-type secondary"
		hostPID = true
	}

	vdev := ""
	for _, value := range app.Eal.Vdevs {
		vdev += " --vdev "
		vdev += strings.Join(value, ",")
	}
	args += vdev

	args += " -- " + app.Args[0]

	return name, args, hostPID
}

// newPodForApp returns an app pod with the same name/namespace as the cr
func (spp *Spp) NewApp(index int) *corev1.Pod {
	node := sppcommon.MakeLabel(sppcommon.WORKER_NODE_LABEL, spp.V1.Status.Node)
	name, args, hostPID := spp.makeAppArgsPipetest(index)
	app := spp.V1.Spec.Apps[index]
	privileged := true
	app_pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      sppcommon.MakeName(spp.V1.Name, name, "-pod"),
			Namespace: spp.V1.Namespace,
		},
		Spec: corev1.PodSpec{
			HostPID:      hostPID,
			NodeSelector: node,
			Containers: []corev1.Container{
				{
					Name:    "container",
					Image:   app.Image,
					Command: []string{"/bin/bash", "-c"},
					SecurityContext: &corev1.SecurityContext{
						Privileged: &privileged,
					},
					Args: []string{args},
					Resources: corev1.ResourceRequirements{
						Limits: sppcommon.ResourcesForHugePage("1Gi"),
					},
					VolumeMounts: []corev1.VolumeMount{
						sppcommon.MakeVolumeMount("hugepages", "/dev/hugepages"),
						sppcommon.MakeVolumeMount("dpdk", "/var/run"),
						sppcommon.MakeVolumeMount("tmp", "/tmp"),
					},
				},
			},
			Volumes: []corev1.Volume{
				sppcommon.MakeVolume("hugepages", "/dev/hugepages"),
				sppcommon.MakeVolume("dpdk", "/var/run"),
				sppcommon.MakeVolume("tmp", "/tmp"),
			},
		},
	}
	return app_pod
}
