package common

import (
	"encoding/json"
	"fmt"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	"net/http"
	"reflect"
	"strings"
	"time"
)

// define spp ctl port number
const (
	CTL_PRI_PORT_NUM = 5555
	CTL_SEC_PORT_NUM = 6666
	CTL_CLI_PORT_NUM = 7777
)

// define workder node labels
const (
	MASTER_NODE_LABEL = "node-role.kubernetes.io/master"
	WORKER_NODE_LABEL = "kubernetes.io/hostname"
)

/*
Spp data
*/
type JsonData map[string]interface{}

/*
common functions
*/

func MakeStatus(keys []reflect.Value) string {
	strkeys := make([]string, len(keys))
	for i := 0; i < len(keys); i++ {
		strkeys[i] = keys[i].String()
	}
	return strings.Join(strkeys, ",")
}

// stringInSlice returns true if a string does not contain a list
func StringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return false
		}
	}
	return true
}

func MakeLabel(key string, value string) map[string]string {
	return map[string]string{key: value}
}

func ResourcesForHugePage(memory string) corev1.ResourceList {
	return corev1.ResourceList{
		"hugepages-1Gi": resource.MustParse(memory),
		"memory":        resource.MustParse(memory),
	}
}

func MakeVolume(name string, path string) corev1.Volume {
	return corev1.Volume{
		Name: name,
		VolumeSource: corev1.VolumeSource{
			HostPath: &corev1.HostPathVolumeSource{
				Path: path,
			},
		},
	}
}

func MakeVolumeMount(name string, path string) corev1.VolumeMount {
	return corev1.VolumeMount{
		Name:      name,
		MountPath: path,
	}
}

func (data *JsonData) Request(method string, url string) bool {
	// timeout 60 seconds
	for count := 0; count < 12; count++ {
		if HttpRequest(method, url, data) {
			fmt.Println("HTTP Request succeeded :", method, url, data)
			return true
		} else {
			fmt.Println("HTTP Request failed    :", method, url, data)
			time.Sleep(5 * time.Second)
		}
	}
	return false
}

func CompareDifference(a, b []*JsonData) []*JsonData {
	result := []*JsonData{}
	// find elements which exist in a but not in b
	for _, i := range a {
		a_not_exist_in_b := true
		for _, j := range b {
			if reflect.DeepEqual(i, j) {
				a_not_exist_in_b = false
				break
			}
		}
		if a_not_exist_in_b {
			result = append(result, i)
		}
	}
	return result
}

func MakeName(resource_name string, name string, kind string) string {
	return resource_name + "-" + name + "-" + kind
}

func GetSecId(name string) (string, string) {
	slice := strings.Split(name, ":")
	return slice[0], slice[1]
}

/*
HTTP request functions
*/
// HTTP Request using Put or Post method
func HttpRequest(method string, url string, data *JsonData) bool {
	bytes, _ := json.Marshal(data)
	payload := strings.NewReader(string(bytes))
	req, _ := http.NewRequest(method, url, payload)
	req.Header.Add("Content-Type", "application/json")
	res, _ := http.DefaultClient.Do(req)
	defer res.Body.Close()
	return res.StatusCode == http.StatusNoContent
}

// HTTP Request using Get method
func HttpDeleteRequest(url string) bool {
	req, _ := http.NewRequest("DELETE", url, nil)
	res, _ := http.DefaultClient.Do(req)
	defer res.Body.Close()
	return res.StatusCode == http.StatusOK
}

// HTTP Request using Get method only status
func HttpGetRequest(url string) bool {
	res, _ := http.Get(url)
	return res.StatusCode == http.StatusOK
}

// HTTP Request using Get method and get a response as json
func HttpGetRequestAsJson(url string, target interface{}) bool {
	myclient := &http.Client{}
	res, err := myclient.Get(url)
	if err != nil {
		fmt.Println("Http response got error : ", err, "Confirm if there is route from this host to ", url)
		return false
	}

	defer res.Body.Close()
	json.NewDecoder(res.Body).Decode(target)
	return res.StatusCode == http.StatusOK
}
