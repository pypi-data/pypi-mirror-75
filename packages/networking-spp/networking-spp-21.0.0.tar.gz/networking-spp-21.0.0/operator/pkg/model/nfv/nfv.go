package nfv

import (
	"fmt"
	sppv1 "opendev.org/x/networking-spp/operator/pkg/apis/spp/v1"
	sppcommon "opendev.org/x/networking-spp/operator/pkg/model/common"
	"reflect"
	"strings"
	"time"
)

// putResources make http request with put method
func PutResources(resource string, base_url string, action string) bool {
	url := base_url + "/ports"
	data := &sppcommon.JsonData{"action": action, "port": resource}

	// flag of res
	successful := false
	// timeout 120 seconds
	for count := 0; count < 12; count++ {
		// check if the nfv is ready
		if sppcommon.HttpGetRequest(base_url) {
			if sppcommon.HttpRequest("PUT", url, data) {
				successful = true
			}
			break
		} else {
			time.Sleep(10 * time.Second)
		}
	}
	fmt.Println("putResources called with data:", data, action, successful)
	return successful
}

// putPatches make http request with put method
func PutPatches(patch sppv1.PatchOption, base_url string) bool {
	url := base_url + "/patches"
	data := &sppcommon.JsonData{"src": patch.Src, "dst": patch.Dst}

	// flag of res
	successful := false
	// check if the nfv is ready
	if sppcommon.HttpGetRequest(base_url) {
		//Do patches
		//for _,  patch := range spp.Cr.Spec.Nfvs[index].Patches {
		if sppcommon.HttpRequest("PUT", url, data) {
			successful = true
		}
	}
	fmt.Println("putPatches called with data:", data, successful)
	return successful
}

// checkResourcesExist returns ture if vhost or ring exist in response
func CheckResourcesExist(response *sppv1.SppNfvResponse) bool {
	for _, resource := range response.Resources {
		if strings.Contains(resource, "vhost") || strings.Contains(resource, "ring") {
			return true
		}
	}
	return false
}

// checkPatchesChanged returns ture if patches has been changed
func CheckPatchesChanged(response *sppv1.SppNfvResponse, patches []sppv1.PatchOption) bool {
	patches_map := []map[string]string{}
	for _, patch := range patches {
		patch_map := map[string]string{"src": patch.Src, "dst": patch.Dst}
		patches_map = append(patches_map, patch_map)
	}

	patch_changed := !reflect.DeepEqual(patches_map, response.Patches)
	fmt.Println("Patches from REST API : ", response.Patches)
	fmt.Println("Patches from CR yaml  : ", patches_map)
	return patch_changed
}

// checkResourcesChanged returns resources deleted and added by comparing response and resources given
func CheckResourcesChanged(response *sppv1.SppNfvResponse, resources []string) ([]string, []string) {
	deleted_resources := []string{}
	added_resources := []string{}

	for _, resource := range resources {
		if strings.Contains(resource, "vhost") || strings.Contains(resource, "ring") {
			if sppcommon.StringInSlice(resource, response.Resources) {
				added_resources = append(added_resources, resource)
			}
		}
	}

	for _, resource := range response.Resources {
		if strings.Contains(resource, "vhost") || strings.Contains(resource, "ring") {
			if sppcommon.StringInSlice(resource, resources) {
				deleted_resources = append(deleted_resources, resource)
			}
		}
	}

	fmt.Println("Resources from REST API: ", response.Resources)
	fmt.Println("Resources from CR yaml : ", resources)
	return deleted_resources, added_resources
}
