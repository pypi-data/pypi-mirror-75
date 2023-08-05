package spp

import (
	"context"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	sppv1 "opendev.org/x/networking-spp/operator/pkg/apis/spp/v1"
	sppmodel "opendev.org/x/networking-spp/operator/pkg/model"
	sppcommon "opendev.org/x/networking-spp/operator/pkg/model/common"
	"reflect"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/handler"
	logf "sigs.k8s.io/controller-runtime/pkg/log"
	"sigs.k8s.io/controller-runtime/pkg/manager"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"
	"sigs.k8s.io/controller-runtime/pkg/source"
	"strconv"
	"time"
)

var log = logf.Log.WithName("controller_spp")

/**
* USER ACTION REQUIRED: This is a scaffold file intended for the user to modify with their own Controller
* business logic.  Delete these comments after modifying this file.*
 */

// Add creates a new Spp Controller and adds it to the Manager. The Manager will set fields on the Controller
// and Start it when the Manager is Started.
func Add(mgr manager.Manager) error {
	return add(mgr, newReconciler(mgr))
}

// newReconciler returns a new reconcile.Reconciler
func newReconciler(mgr manager.Manager) reconcile.Reconciler {
	return &ReconcileSpp{client: mgr.GetClient(), scheme: mgr.GetScheme()}
}

// add adds a new Controller to mgr with r as the reconcile.Reconciler
func add(mgr manager.Manager, r reconcile.Reconciler) error {
	// V1.ate a new controller
	c, err := controller.New("spp-controller", mgr, controller.Options{Reconciler: r})
	if err != nil {
		return err
	}

	// Watch for changes to primary resource Spp
	err = c.Watch(&source.Kind{Type: &sppv1.Spp{}}, &handler.EnqueueRequestForObject{})
	if err != nil {
		return err
	}

	// TODO(user): Modify this to be the types you create that are owned by the primary resource
	// Watch for changes to secondary resource Pods and requeue the owner Spp
	err = c.Watch(&source.Kind{Type: &corev1.Pod{}}, &handler.EnqueueRequestForOwner{
		IsController: true,
		OwnerType:    &sppv1.Spp{},
	})
	if err != nil {
		return err
	}
	err = c.Watch(&source.Kind{Type: &corev1.Service{}}, &handler.EnqueueRequestForOwner{
		IsController: true,
		OwnerType:    &sppv1.Spp{},
	})
	if err != nil {
		return err
	}

	return nil
}

// blank assignment to verify that ReconcileSpp implements reconcile.Reconciler
var _ reconcile.Reconciler = &ReconcileSpp{}

// ReconcileSpp reconciles a Spp object
type ReconcileSpp struct {
	// This client, initialized using mgr.Client() above, is a split client
	// that reads objects from the cache and writes to the apiserver
	client client.Client
	scheme *runtime.Scheme
}

func (r *ReconcileSpp) CreateService(spp *sppmodel.Spp, service *corev1.Service) (*corev1.Service, error) {
	reqLogger := log.WithValues()
	found_service := &corev1.Service{}

	// See the as the owner and controller
	if err := controllerutil.SetControllerReference(spp.V1, service, r.scheme); err != nil {
		return found_service, err
	}

	// Check if the pod already exists
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: service.Name, Namespace: service.Namespace}, found_service)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating a new Service", "Service Name", service.Name, "Service Spec", service.Spec)
		err = r.client.Create(context.TODO(), service)
		if err != nil {
			return found_service, err
		}

		// Pod created successfully - don't requeue
		return found_service, nil
	} else if err != nil {
		return found_service, err
	}
	return found_service, nil
}

func (r *ReconcileSpp) FindPod(pod_namespace string, pod_name string) (*corev1.Pod, error) {
	found_pod := &corev1.Pod{}

	// Check if the pod already exists
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: pod_name, Namespace: pod_namespace}, found_pod)
	if err != nil {
		return found_pod, err
	}
	return found_pod, nil
}

/*
func (r *ReconcileSpp) GetNode() (*corev1.NodeList, error) {
        found_node := &corev1.NodeList{}

        // Check if the pod already exists
        err := r.client.Get(context.TODO(), types.NamespacedName{Namespace: "default"}, found_node)
        if err != nil {
                return found_node, err
        }

        opts := []client.ListOption{
            client.InNamespace("default"),
	    client.MatchingLabels{"app", request.NamespacedName.Name},
	    client.MatchingFields{"status.phase": "Running"},
            //client.InNamespace("default"),
            //client.MatchingLabels{"app", "default"},
        }

        err := r.client.List(context.TODO(), found_node, opts)
        return found_node, nil
}
*/

func (r *ReconcileSpp) CreatePod(spp *sppmodel.Spp, pod *corev1.Pod) (*corev1.Pod, error) {
	reqLogger := log.WithValues()
	found_pod := &corev1.Pod{}

	// See the as the owner and controller
	if err := controllerutil.SetControllerReference(spp.V1, pod, r.scheme); err != nil {
		return found_pod, err
	}

	// Check if the pod already exists
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: pod.Name, Namespace: pod.Namespace}, found_pod)
	if err != nil && errors.IsNotFound(err) {
		reqLogger.Info("Creating a new Pod", "Pod Name", pod.Name, "Pod Spec", pod.Spec)
		err = r.client.Create(context.TODO(), pod)
		if err != nil {
			return found_pod, err
		}

		// Pod created successfully - don't requeue
		return found_pod, nil
	} else if err != nil {
		return found_pod, err
	}
	return found_pod, nil
}

func (r *ReconcileSpp) DeletePod(pod *corev1.Pod) (*corev1.Pod, error) {
	reqLogger := log.WithValues()
	found_pod := &corev1.Pod{}

	// Check if the Pod already exists then delete
	err := r.client.Get(context.TODO(), types.NamespacedName{Name: pod.Name, Namespace: pod.Namespace}, found_pod)
	if err == nil {
		reqLogger.Info("Deleted an old Pod", "Pod Name", pod.Name, "Pod Spec", pod.Spec)
		err = r.client.Delete(context.TODO(), pod)
		if err != nil {
			return found_pod, err
		}

		// Pod deleted successfully - don't requeue
		return found_pod, nil
	} else if err != nil {
		return found_pod, err
	}
	return found_pod, nil
}

func (r *ReconcileSpp) DetermineWorkerNode(spp *sppmodel.Spp) string {
	//Get Node list
	//label := map[string]string{"node-role.kubernetes.io/master": ""}
	nodeList := &corev1.NodeList{}
	listOpts := []client.ListOption{
		//client.InNamespace(spp.V1.Namespace),
		//client.MatchingLabels(label),
	}
	r.client.List(context.TODO(), nodeList, listOpts...)

	//Get spp list
	spplist := &sppv1.SppList{}
	r.client.List(context.TODO(), spplist, listOpts...)

	node_label := ""
	for _, node := range nodeList.Items {
		is_used := false

		// Skip if master node
		if _, ok := node.Labels[sppcommon.MASTER_NODE_LABEL]; ok {
			continue
		}

		//Search all spp resources
		for _, spp_v1 := range spplist.Items {
			//Skip if itself
			if spp_v1.Name == spp.V1.Name {
				continue
			}
			if spp_v1.Status.Node == node.Labels[sppcommon.WORKER_NODE_LABEL] {
				is_used = true
				break
			}
		}

		if !is_used {
			node_label = node.Labels[sppcommon.WORKER_NODE_LABEL]
			break
		}
	}

	return node_label
}

// Reconcile reads that state of the cluster for a Spp object and makes changes based on the state read
// and what is in the Spp.Spec
// TODO(user): Modify this Reconcile function to implement your Controller logic.  This example creates
// a Pod as an example
// Note:
// The Controller will requeue the Request to be processed again if the returned error is non-nil or
// Result.Requeue is true, otherwise upon completion it will remove the work from the queue.
func (r *ReconcileSpp) Reconcile(request reconcile.Request) (reconcile.Result, error) {
	// Log
	reqLogger := log.WithValues("Request.Namespace", request.Namespace, "Request.Name", request.Name)
	reqLogger.Info("Reconciling Spp")

	// Fetch the Spp Costum Resource from the yaml file
	spp := &sppmodel.Spp{}
	spp.V1 = &sppv1.Spp{}

	err := r.client.Get(context.TODO(), request.NamespacedName, spp.V1)
	if err != nil {
		if errors.IsNotFound(err) {
			// Request object not found, could have been deleted after reconcile request.
			// Owned objects are automatically garbage collected. For additional cleanup logic use finalizers.
			// Return and don't requeue
			return reconcile.Result{}, nil
		}
		// Error reading the object - requeue the request.
		return reconcile.Result{}, err
	}
	reqLogger.Info("Spp V1", "Spec", spp.V1.Spec)
	reqLogger.Info("Spp V1", "Status", spp.V1.Status)

	//Determine worker node
	if spp.V1.Status.Node == "" {
		spp.V1.Status.Node = r.DetermineWorkerNode(spp)
		reqLogger.Info("Spp V1", "Worker Node Determined", spp.V1.Status.Node)
	} else {
		reqLogger.Info("Spp V1", "Worker Node", spp.V1.Status.Node)
	}

	// Create Ctl Pod and Service, Check ctl status and service-vip and Update Status
	ctl_pod, ctl_service := spp.NewCtl()
	found_ctl_pod, err := r.CreatePod(spp, ctl_pod)
	if err != nil {
		return reconcile.Result{}, err
	}
	found_ctl_service, err := r.CreateService(spp, ctl_service)
	if err != nil {
		return reconcile.Result{}, err
	}
	spp.V1.Status.Ctl.Pods.Name = found_ctl_pod.Name
	spp.V1.Status.ServiceVip = found_ctl_service.Spec.ClusterIP
	//spp.V1.Status.Node = found_ctl_pod.Status.HostIP
	if !reflect.DeepEqual(found_ctl_pod.Status.Phase, spp.V1.Status.Ctl.Pods.Phase) {
		spp.V1.Status.Ctl.Pods.Phase = found_ctl_pod.Status.Phase
		spp.V1.Status.Primary.Status = "0/1"
		r.client.Status().Update(context.TODO(), spp.V1)
	}

	// Checck if Ctl Pod is running and CTL Service are active using REST API
	//if found_ctl_pod.Status.Phase == "Running" && spp.CheckCtlRunning(6) {
	if found_ctl_pod.Status.Phase == "Running" && spp.CheckRunning("ctl", 6) {
		// Update ctl status
		if reflect.DeepEqual(spp.V1.Status.Ctl.Status, "0/1") {
			spp.V1.Status.Ctl.Status = "1/1"
			spp.V1.Status.Status = "Ctl is ready"
			spp.V1.Status.Events = append(spp.V1.Status.Events, "Ctl is created")
			r.client.Status().Update(context.TODO(), spp.V1)
		}

		// Create a Primary Pod and Update status
		found_primary_pod, err := r.CreatePod(spp, spp.NewPrimary())
		if err != nil {
			return reconcile.Result{}, err
		}
		spp.V1.Status.Primary.Pods.Name = found_primary_pod.Name
		if !reflect.DeepEqual(found_primary_pod.Status.Phase, spp.V1.Status.Primary.Pods.Phase) {
			spp.V1.Status.Primary.Pods.Phase = found_primary_pod.Status.Phase
			r.client.Status().Update(context.TODO(), spp.V1)
		}

		// Check if Primary is active using REST API
		//if spp.CheckPrimaryRunning(6) {
		if spp.CheckRunning("primary", 6) {
			//Update primary status
			if reflect.DeepEqual(spp.V1.Status.Primary.Status, "0/1") {
				spp.V1.Status.Primary.Status = "1/1"
				spp.V1.Status.Primary.Pods.Phase = found_primary_pod.Status.Phase
				spp.V1.Status.Status = "Primary is ready"
				spp.V1.Status.Events = append(spp.V1.Status.Events, "Primary is created")
				r.client.Status().Update(context.TODO(), spp.V1)
			}

			//  NFVS
			// Init nfv status
			if spp.V1.Status.Nfvs.Pods == nil {
				spp.V1.Status.Nfvs.Pods = map[string]*sppv1.SppStatusPodNfv{}
			} else {
				// Delete Nfv Pods which deleted from yaml
				for _, secId := range spp.OldNfvs() {
					// Delete the Pod all resources
					spp.BeforeDeleteNfv(secId)

					//Find Pod and Delete it
					found_pod, err := r.FindPod(spp.V1.Namespace, spp.V1.Status.Nfvs.Pods[secId].Name)
					if err != nil {
						return reconcile.Result{}, err
					}
					_, err = r.DeletePod(found_pod)
					if err != nil {
						return reconcile.Result{}, err
					}

					//Delete nfv from status and tell spp controller the nfv is deleted
					delete(spp.V1.Status.Nfvs.Pods, secId)
					spp.V1.Status.Status = "Nfvs ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Nfvs.Pods).MapKeys())
					spp.V1.Status.Events = append(spp.V1.Status.Events, "Nfv "+secId+" is deleted")
					spp.Delete("nfv", secId)
					r.client.Status().Update(context.TODO(), spp.V1)
				}
			}
			//Create Nfv Pods which added from yaml
			for i, nfv := range spp.V1.Spec.Nfvs {
				_, secId := sppcommon.GetSecId(spp.V1.Spec.Nfvs[i].Name)

				// Create Pod
				found_nfv_pod, err := r.CreatePod(spp, spp.NewNfv(i))
				if err != nil {
					return reconcile.Result{}, err
				}

				// Only reconcile the found nfv pods which are running
				if found_nfv_pod.Status.Phase == "Running" {
					response := spp.ReconcileNfv(secId, &nfv)
					reqLogger.Info("The Nfv Pod ", "Response", response)

					//Get new status
					nfv_pod_status := &sppv1.SppStatusPodNfv{Name: found_nfv_pod.Name, Phase: found_nfv_pod.Status.Phase, Response: response}
					//Update nfv status
					if !reflect.DeepEqual(spp.V1.Status.Nfvs.Pods[secId], nfv_pod_status) {
						reqLogger.Info("Current Running Nfv Pods", "Nfv Pods", spp.V1.Status.Nfvs.Pods[secId])
						spp.V1.Status.Nfvs.Pods[secId] = nfv_pod_status
						spp.V1.Status.Status = "Nfvs ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Nfvs.Pods).MapKeys())
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else if found_nfv_pod.Name != "" {
					if len(spp.V1.Status.Nfvs.Pods) < len(spp.V1.Spec.Nfvs) {
						nfv_pod_status := &sppv1.SppStatusPodNfv{Name: found_nfv_pod.Name, Phase: found_nfv_pod.Status.Phase, Response: nil}
						spp.V1.Status.Nfvs.Pods[secId] = nfv_pod_status
						spp.V1.Status.Events = append(spp.V1.Status.Events, "Nfv "+secId+" is created")
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else {
					reqLogger.Info("The Nfv Pod is not Running but still exists in CR", "Nfv Pod Name", found_nfv_pod.Name)
				}
			}
			//Update nfv status
			nfvs_status := strconv.Itoa(len(spp.V1.Status.Nfvs.Pods)) + "/" + strconv.Itoa(len(spp.V1.Spec.Nfvs))
			if !reflect.DeepEqual(spp.V1.Status.Nfvs.Status, nfvs_status) {
				spp.V1.Status.Nfvs.Status = nfvs_status
				r.client.Status().Update(context.TODO(), spp.V1)
			}
			// END of NFV

			//  VFS
			// Init vf status
			if spp.V1.Status.Vfs.Pods == nil {
				spp.V1.Status.Vfs.Pods = map[string]*sppv1.SppStatusPodVf{}
			} else {
				// Delete Vf Pods which deleted from yaml
				for _, secId := range spp.Olds("vf") {

					//Find Pod and Delete it
					found_pod, err := r.FindPod(spp.V1.Namespace, spp.V1.Status.Vfs.Pods[secId].Name)
					if err != nil {
						return reconcile.Result{}, err
					}
					_, err = r.DeletePod(found_pod)
					if err != nil {
						return reconcile.Result{}, err
					}

					//Delete vf from status and tell spp controller the vf is deleted
					delete(spp.V1.Status.Vfs.Pods, secId)
					spp.V1.Status.Status = "Vfs ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Vfs.Pods).MapKeys())
					spp.V1.Status.Events = append(spp.V1.Status.Events, "Vf "+secId+" is deleted")
					spp.Delete("vf", secId)
					r.client.Status().Update(context.TODO(), spp.V1)
				}
			}
			//Create Vf Pods which added from yaml
			for i, vf := range spp.V1.Spec.Vfs {
				_, secId := sppcommon.GetSecId(spp.V1.Spec.Vfs[i].Name)

				// Create Pod
				found_vf_pod, err := r.CreatePod(spp, spp.NewVf(i))
				if err != nil {
					return reconcile.Result{}, err
				}

				// Only reconcile the found vf pods which are running
				if found_vf_pod.Status.Phase == "Running" {
					//response := spp.Reconcile(secId, &vf)
					response := spp.Reconcile(secId, "vf", vf.Components, vf.ClassifierTable)

					reqLogger.Info("The Vf Pod ", "Response", response)

					//Get new status
					vf_pod_status := &sppv1.SppStatusPodVf{Name: found_vf_pod.Name, Phase: found_vf_pod.Status.Phase, Response: response}
					//Update vf status
					if !reflect.DeepEqual(spp.V1.Status.Vfs.Pods[secId], vf_pod_status) {
						reqLogger.Info("Current Running Vf Pods", "Vf Pods", spp.V1.Status.Vfs.Pods[secId])
						spp.V1.Status.Vfs.Pods[secId] = vf_pod_status
						spp.V1.Status.Status = "Vfs ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Vfs.Pods).MapKeys())
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else if found_vf_pod.Name != "" {
					if len(spp.V1.Status.Vfs.Pods) < len(spp.V1.Spec.Vfs) {
						//vf_pod_status := &sppv1.SppStatusPodVf{Name:found_vf_pod.Name, Phase:found_vf_pod.Status.Phase, Response:nil}
						spp.V1.Status.Vfs.Pods[secId] = &sppv1.SppStatusPodVf{Name: found_vf_pod.Name, Phase: found_vf_pod.Status.Phase, Response: nil}
						spp.V1.Status.Events = append(spp.V1.Status.Events, "Vf "+secId+" is created")
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else {
					reqLogger.Info("The Vf Pod is not Running but still exists in CR", "Vf Pod Name", found_vf_pod.Name)
				}
			}
			//Update vf status
			vfs_status := strconv.Itoa(len(spp.V1.Status.Vfs.Pods)) + "/" + strconv.Itoa(len(spp.V1.Spec.Vfs))
			if !reflect.DeepEqual(spp.V1.Status.Vfs.Status, vfs_status) {
				spp.V1.Status.Vfs.Status = vfs_status
				r.client.Status().Update(context.TODO(), spp.V1)
			}
			// END of VF

			//  MIRRORS
			// Init mirror status
			if spp.V1.Status.Mirrors.Pods == nil {
				spp.V1.Status.Mirrors.Pods = map[string]*sppv1.SppStatusPodVf{}
			} else {
				// Delete Mirror Pods which deleted from yaml
				for _, secId := range spp.Olds("mirror") {

					//Find Pod and Delete it
					found_pod, err := r.FindPod(spp.V1.Namespace, spp.V1.Status.Mirrors.Pods[secId].Name)
					if err != nil {
						return reconcile.Result{}, err
					}
					_, err = r.DeletePod(found_pod)
					if err != nil {
						return reconcile.Result{}, err
					}

					//Delete mirror from status and tell spp controller the mirror is deleted
					delete(spp.V1.Status.Mirrors.Pods, secId)
					spp.V1.Status.Status = "Mirrors ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Mirrors.Pods).MapKeys())
					spp.V1.Status.Events = append(spp.V1.Status.Events, "Mirror "+secId+" is deleted")
					spp.Delete("mirror", secId)
					r.client.Status().Update(context.TODO(), spp.V1)
				}
			}
			//Create Mirror Pods which added from yaml
			for i, mirror := range spp.V1.Spec.Mirrors {
				_, secId := sppcommon.GetSecId(spp.V1.Spec.Mirrors[i].Name)

				// Create Pod
				found_mirror_pod, err := r.CreatePod(spp, spp.NewMirror(i))
				if err != nil {
					return reconcile.Result{}, err
				}

				// Only reconcile the found mirror pods which are running
				if found_mirror_pod.Status.Phase == "Running" {
					//response := spp.Reconcile(secId, &vf)
					response := spp.Reconcile(secId, "mirror", mirror.Components, nil)

					reqLogger.Info("The Mirror Pod ", "Response", response)

					//Get new status
					mirror_pod_status := &sppv1.SppStatusPodVf{Name: found_mirror_pod.Name, Phase: found_mirror_pod.Status.Phase, Response: response}
					//Update mirror status
					if !reflect.DeepEqual(spp.V1.Status.Mirrors.Pods[secId], mirror_pod_status) {
						reqLogger.Info("Current Running Mirror Pods", "Mirror Pods", spp.V1.Status.Mirrors.Pods[secId])
						spp.V1.Status.Mirrors.Pods[secId] = mirror_pod_status
						spp.V1.Status.Status = "Mirrors ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Mirrors.Pods).MapKeys())
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else if found_mirror_pod.Name != "" {
					if len(spp.V1.Status.Mirrors.Pods) < len(spp.V1.Spec.Mirrors) {
						//vf_pod_status := &sppv1.SppStatusPodVf{Name:found_vf_pod.Name, Phase:found_vf_pod.Status.Phase, Response:nil}
						spp.V1.Status.Mirrors.Pods[secId] = &sppv1.SppStatusPodVf{Name: found_mirror_pod.Name, Phase: found_mirror_pod.Status.Phase, Response: nil}
						spp.V1.Status.Events = append(spp.V1.Status.Events, "Mirror "+secId+" is created")
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else {
					reqLogger.Info("The Mirror Pod is not Running but still exists in CR", "Mirror Pod Name", found_mirror_pod.Name)
				}
			}
			//Update mirror status
			mirrors_status := strconv.Itoa(len(spp.V1.Status.Mirrors.Pods)) + "/" + strconv.Itoa(len(spp.V1.Spec.Mirrors))
			if !reflect.DeepEqual(spp.V1.Status.Mirrors.Status, mirrors_status) {
				spp.V1.Status.Mirrors.Status = mirrors_status
				r.client.Status().Update(context.TODO(), spp.V1)
			}
			// END of MIRROR

			//  PCAP
			// Init pcap status
			if spp.V1.Status.Pcaps.Pods == nil {
				spp.V1.Status.Pcaps.Pods = map[string]*sppv1.SppStatusPodPcap{}
			} else {
				// Delete pcap Pods which deleted from yaml
				for _, secId := range spp.OldPcaps() {

					//Find Pod and Delete it
					found_pod, err := r.FindPod(spp.V1.Namespace, spp.V1.Status.Pcaps.Pods[secId].Name)
					if err != nil {
						return reconcile.Result{}, err
					}
					_, err = r.DeletePod(found_pod)
					if err != nil {
						return reconcile.Result{}, err
					}

					//Delete pcap from status and tell spp controller the pcap is deleted
					delete(spp.V1.Status.Pcaps.Pods, secId)
					spp.V1.Status.Status = "Pcaps ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Pcaps.Pods).MapKeys())
					spp.V1.Status.Events = append(spp.V1.Status.Events, "Pcap "+secId+" is deleted")
					spp.Delete("pcap", secId)
					r.client.Status().Update(context.TODO(), spp.V1)
				}
			}
			//Create Pcap Pods which added from yaml
			for i, pcap := range spp.V1.Spec.Pcaps {
				_, secId := sppcommon.GetSecId(spp.V1.Spec.Pcaps[i].Name)

				// Create Pod
				found_pcap_pod, err := r.CreatePod(spp, spp.NewPcap(i))
				if err != nil {
					return reconcile.Result{}, err
				}

				// Only reconcile the found pcap pods which are running
				if found_pcap_pod.Status.Phase == "Running" {
					response := spp.ReconcilePcap(secId, &pcap)
					reqLogger.Info("The Pcap Pod ", "Response", response)

					//Get new status
					pcap_pod_status := &sppv1.SppStatusPodPcap{Name: found_pcap_pod.Name, Phase: found_pcap_pod.Status.Phase, Response: response}
					//Update pcap status
					if !reflect.DeepEqual(spp.V1.Status.Pcaps.Pods[secId], pcap_pod_status) {
						reqLogger.Info("Current Running Pcap Pods", "Pcap Pods", spp.V1.Status.Pcaps.Pods[secId])
						spp.V1.Status.Pcaps.Pods[secId] = pcap_pod_status
						spp.V1.Status.Status = "Pcaps ready ids:" + sppcommon.MakeStatus(reflect.ValueOf(spp.V1.Status.Pcaps.Pods).MapKeys())
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else if found_pcap_pod.Name != "" {
					if len(spp.V1.Status.Pcaps.Pods) < len(spp.V1.Spec.Pcaps) {
						spp.V1.Status.Pcaps.Pods[secId] = &sppv1.SppStatusPodPcap{Name: found_pcap_pod.Name, Phase: found_pcap_pod.Status.Phase, Response: nil}
						spp.V1.Status.Events = append(spp.V1.Status.Events, "Pcap "+secId+" is created")
						r.client.Status().Update(context.TODO(), spp.V1)
					}
				} else {
					reqLogger.Info("The Pcap Pod is not Running but still exists in CR", "Pcap Pod Name", found_pcap_pod.Name)
				}
			}
			//Update pcap status
			pcaps_status := strconv.Itoa(len(spp.V1.Status.Pcaps.Pods)) + "/" + strconv.Itoa(len(spp.V1.Spec.Pcaps))
			if !reflect.DeepEqual(spp.V1.Status.Pcaps.Status, pcaps_status) {
				spp.V1.Status.Pcaps.Status = pcaps_status
				r.client.Status().Update(context.TODO(), spp.V1)
			}
			// END of PCAP

			// APPS
			// all nfvs, vfs ,mirrors are ready(forward) then run apps
			if spp.CheckReady() {
				if spp.V1.Status.Apps.Pods == nil {
					//pods := make(sppv1.SppStatusPodBasic, 10)
					//spp.V1.Status.Apps = sppv1.SppStatusApp{Pods:pods}
					//spp.V1.Status.Apps.Pods = []sppv1.SppStatusPodBasic{}
					spp.V1.Status.Apps.Pods = make([]sppv1.SppStatusPodBasic, len(spp.V1.Spec.Apps))
				}
				reqLogger.Info("Ready to create apps")
				// V1.ate app pods
				for i, _ := range spp.V1.Spec.Apps {
					//Update events
					event := spp.V1.Spec.Apps[i].Name + " is created."
					spp.V1.Status.Status = spp.V1.Spec.Apps[i].Name + " is ready"
					spp.V1.Status.Events = append(spp.V1.Status.Events, event)

					for count := 0; count < 12; count++ {
						app_pod, err := r.CreatePod(spp, spp.NewApp(i))

						//Update apps status
						if !reflect.DeepEqual(spp.V1.Status.Apps.Pods[i].Phase, app_pod.Status.Phase) {
							spp.V1.Status.Apps.Pods[i].Name = app_pod.Name
							spp.V1.Status.Apps.Pods[i].Phase = app_pod.Status.Phase
							r.client.Status().Update(context.TODO(), spp.V1)
						}

						if err != nil {
							return reconcile.Result{}, err
						}

						if app_pod.Status.Phase == "Running" {
							break
						} else {
							time.Sleep(5 * time.Second)
						}

						//Update app status
						apps_status := strconv.Itoa(i+1) + "/" + strconv.Itoa(len(spp.V1.Spec.Apps))
						if !reflect.DeepEqual(spp.V1.Status.Apps.Status, apps_status) {
							spp.V1.Status.Apps.Status = apps_status
							r.client.Status().Update(context.TODO(), spp.V1)
						}
					}
				}
			}
			// END of APPS

		} else {
			if !reflect.DeepEqual(spp.V1.Status.Primary.Status, "0/1") {
				spp.V1.Status.Primary.Status = "0/1"
				spp.V1.Status.Primary.Pods.Phase = found_primary_pod.Status.Phase
				r.client.Status().Update(context.TODO(), spp.V1)
			}
		}

		//Log primary status
		reqLogger.Info("Primary Pod", "Phase", found_primary_pod.Status.Phase)
	} else {
		//Update ctl status
		if !reflect.DeepEqual(spp.V1.Status.Ctl.Status, "0/1") {
			spp.V1.Status.Status = "Pending"
			spp.V1.Status.Ctl.Status = "0/1"
			r.client.Status().Update(context.TODO(), spp.V1)
		}
	}

	// Log Ctl pod and service vip
	reqLogger.Info("CTL Pod", "Phase", spp.V1.Status.Ctl.Pods.Phase)
	reqLogger.Info("CTL Service", "VIP", spp.V1.Status.ServiceVip)

	return reconcile.Result{}, nil
}
