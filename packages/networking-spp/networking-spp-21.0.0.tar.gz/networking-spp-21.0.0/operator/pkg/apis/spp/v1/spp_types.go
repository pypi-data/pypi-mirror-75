package v1

import (
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

/*
Custom resource for Spp Spec
*/

// VdevOption defines Vdev option
type VdevOption []string

// ResourceOption defines Resources option
type ResourceOption []string

//PatchOption defines Patches
type PatchOption struct {
	Src string `json:"src"`
	Dst string `json:"dst"`
}

//EalOption defines EAL options
type EalOption struct {
	Lcores    string       `json:"lcores"`
	SocketMem string       `json:"socket-mem"`
	Vdevs     []VdevOption `json:"vdevs"`
}

//SppApp defines SPP App options
type SppApp struct {
	Name    string    `json:"name"`
	Image   string    `json:"image"`
	Command []string  `json:"command"`
	Args    []string  `json:"args"`
	Type    string    `json:"type"`
	Eal     EalOption `json:"eal"`
}

type VlanOption struct {
	Operation string `json:"operation"`
	Id        int    `json:"id"`
	Pcp       int    `json:"pcp"`
}

type PortOption struct {
	Port string     `json:"port"`
	Vlan VlanOption `json:"vlan"`
}

type ClassifierTableOption struct {
	Type  string `json:"type"`
	Value string `json:"value"`
	Vlan  int    `json:"vlan"`
	Port  string `json:"port"`
}

type ComponentOption struct {
	Core   int          `json:"core"`
	Name   string       `json:"name"`
	RxPort []PortOption `json:"rx_port"`
	TxPort []PortOption `json:"tx_port"`
	Type   string       `json:"type"`
}

//SppVf defines SPP VF options
type SppVf struct {
	Name            string                  `json:"name"`
	Image           string                  `json:"image"`
	Eal             EalOption               `json:"eal"`
	Components      []ComponentOption       `json:"components"`
	ClassifierTable []ClassifierTableOption `json:"classifier_table"`
}

//SppMirror defines SPP Mirror options
type SppMirror struct {
	Name       string            `json:"name"`
	Image      string            `json:"image"`
	Eal        EalOption         `json:"eal"`
	Components []ComponentOption `json:"components"`
}

type SppPcap struct {
	Name   string    `json:"name"`
	Image  string    `json:"image"`
	Eal    EalOption `json:"eal"`
	Port   string    `json:"port"`
	Status string    `json:"status"`
	OutDir string    `json:"out_dir"`
	Fsize  int       `json:"fsize"`
}

//SppPrimary defines SPP NFV options
type SppNfv struct {
	Name      string         `json:"name"`
	Image     string         `json:"image"`
	Eal       EalOption      `json:"eal"`
	Vhost     string         `json:"vhost"`
	Resources ResourceOption `json:"resources"`
	Patches   []PatchOption  `json:"patches"`
}

//SppPrimary defines SPP Primary options
type SppPrimary struct {
	Name     string    `json:"name"`
	Image    string    `json:"image"`
	Eal      EalOption `json:"eal"`
	PortMask string    `json:"portmask"`
}

// SppCtl defines SPP Ctl options
type SppCtl struct {
	Name  string `json:"name"`
	Image string `json:"image"`
}

// SppSpec defines the desired state of Spp
type SppSpec struct {
	// INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
	// Important: Run "operator-sdk generate k8s" to regenerate code after modifying this file
	// Add custom validation using kubebuilder tags: https://book-v1.book.kubebuilder.io/beyond_basics/generating_crd.html
	Ctl     SppCtl      `json:"ctl"`
	Primary SppPrimary  `json:"primary"`
	Nfvs    []SppNfv    `json:"nfvs"`
	Vfs     []SppVf     `json:"vfs"`
	Mirrors []SppMirror `json:"mirrors"`
	Pcaps   []SppPcap   `json:"pcaps"`
	Apps    []SppApp    `json:"apps"`
}

/*  Response for Spp Status  */

// Spp Process  response
type SppProcessResponse struct {
	Type     string `json:"type"`
	ClientId int    `json:"client-id"`
}

/*
Basic (Spp ctl, priamry and apps)
*/
//SppStatusPodBasic
type SppStatusPodBasic struct {
	Name  string          `json:"name"`
	Phase corev1.PodPhase `json:"phase"`
}

// SppStatusBasic
type SppStatusBasic struct {
	Status string            `json:"status"`
	Pods   SppStatusPodBasic `json:"pods"`
}

// SppStatusApp
type SppStatusApp struct {
	Status string              `json:"status"`
	Pods   []SppStatusPodBasic `json:"pods"`
}

/*
NVF
*/
//Response referred to spp model
type SppNfvResponse struct {
	ClientId  int                 `json:"client-id"`
	Status    string              `json:"status"`
	Resources []string            `json:"ports"`
	Patches   []map[string]string `json:"patches"`
}

//Pod Status
type SppStatusPodNfv struct {
	Name     string          `json:"name"`
	Phase    corev1.PodPhase `json:"phase"`
	Response *SppNfvResponse `json:"response"`
}

// Nfv Status
type SppStatusNfv struct {
	Status string                      `json:"status"`
	Pods   map[string]*SppStatusPodNfv `json:"pods"`
	//Pods []SppStatusPodNfv `json:"pods"`
}

/*
VF and Mirror
*/
//Part of response referred to spp model
type VlanResponse struct {
	Operation string `json:"operation"`
	Id        int    `json:"id"`
	Pcp       int    `json:"pcp"`
}
type PortResponse struct {
	Port string       `json:"port"`
	Vlan VlanResponse `json:"vlan"`
}
type ComponentResponse struct {
	Core   int            `json:"core"`
	Name   string         `json:"name"`
	Type   string         `json:"type"`
	RxPort []PortResponse `json:"rx_port"`
	TxPort []PortResponse `json:"tx_port"`
}
type ClassifierTableResponse struct {
	Type  string `json:"type"`
	Value string `json:"value"`
	Port  string `json:"port"`
	Vlan  int    `json:"vlan"`
}

//Response referred to spp model
type SppVfResponse struct {
	ClientId        int                       `json:"client-id"`
	Ports           []string                  `json:"ports"`
	Components      []ComponentResponse       `json:"components"`
	ClassifierTable []ClassifierTableResponse `json:"classifier_table"`
}

//Pod Status
type SppStatusPodVf struct {
	Name     string          `json:"name"`
	Phase    corev1.PodPhase `json:"phase"`
	Response *SppVfResponse  `json:"response"`
}

// VF or Mirror Status
type SppStatusVf struct {
	Status string                     `json:"status"`
	Pods   map[string]*SppStatusPodVf `json:"pods"`
}

func (res *SppVfResponse) FindDeletedPorts(i int) {
}

/*
PCAP
*/
//Response referred to spp model
type SppPcapResponse struct {
	ClientId int    `json:"client-id"`
	Status   string `json:"status"`
}

//Pod Status
type SppStatusPodPcap struct {
	Name     string           `json:"name"`
	Phase    corev1.PodPhase  `json:"phase"`
	Response *SppPcapResponse `json:"response"`
}

//Pcap Status
type SppStatusPcap struct {
	Status string                       `json:"status"`
	Pods   map[string]*SppStatusPodPcap `json:"pods"`
}

// SppStatus defines the observed state of Spp
type SppStatus struct {
	// INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
	// Important: Run "operator-sdk generate k8s" to regenerate code after modifying this file
	// Add custom validation using kubebuilder tags: https://book-v1.book.kubebuilder.io/beyond_basics/generating_crd.html
	Ctl        SppStatusBasic `json:"ctl"`
	Primary    SppStatusBasic `json:"primary"`
	Nfvs       SppStatusNfv   `json:"nfvs"`
	Vfs        SppStatusVf    `json:"vfs"`
	Mirrors    SppStatusVf    `json:"mirrors"`
	Pcaps      SppStatusPcap  `json:"pcaps"`
	Apps       SppStatusApp   `json:"apps"`
	Node       string         `json:"node"`
	ServiceVip string         `json:"service-vip"`
	Status     string         `json:"status"`
	Events     []string       `json:"events"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// Spp is the Schema for the spps API
// +kubebuilder:subresource:status
// +kubebuilder:resource:path=spps,scope=Namespaced
type Spp struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   SppSpec   `json:"spec,omitempty"`
	Status SppStatus `json:"status,omitempty"`
}

// +k8s:deepcopy-gen:interfaces=k8s.io/apimachinery/pkg/runtime.Object

// SppList contains a list of Spp
type SppList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Spp `json:"items"`
}

func init() {
	SchemeBuilder.Register(&Spp{}, &SppList{})
}
