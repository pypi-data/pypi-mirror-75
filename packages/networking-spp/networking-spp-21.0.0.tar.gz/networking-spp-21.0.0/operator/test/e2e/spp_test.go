package e2e

import (
	goctx "context"
	"fmt"
	"net/http"
	"testing"
	"time"

	framework "github.com/operator-framework/operator-sdk/pkg/test"
	"github.com/operator-framework/operator-sdk/pkg/test/e2eutil"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	"opendev.org/x/networking-spp/operator/pkg/apis"
	operator "opendev.org/x/networking-spp/operator/pkg/apis/spp/v1"
)

var (
	retryInterval        = time.Second * 5
	timeout              = time.Second * 60
	cleanupRetryInterval = time.Second * 1
	cleanupTimeout       = time.Second * 5
)

func TestSpp(t *testing.T) {
	sppList := &operator.SppList{
		TypeMeta: metav1.TypeMeta{
			Kind:       "Spp",
			APIVersion: "spp.spp/v1",
		},
	}
	err := framework.AddToFrameworkScheme(apis.AddToScheme, sppList)
	if err != nil {
		t.Fatalf("failed to add custom resource scheme to framework: %v", err)
	}
	// run subtests
	t.Run("spp-operator", func(t *testing.T) {
		t.Run("Cluster", SppCluster)
	})
}

func SppCluster(t *testing.T) {
	t.Parallel()
	ctx := framework.NewTestCtx(t)
	defer ctx.Cleanup()
	err := ctx.InitializeClusterResources(&framework.CleanupOptions{TestContext: ctx, Timeout: cleanupTimeout, RetryInterval: cleanupRetryInterval})
	if err != nil {
		t.Fatalf("failed to initialize cluster resources: %v", err)
	}
	t.Log("Initialized cluster resources")
	namespace, err := ctx.GetNamespace()
	if err != nil {
		t.Fatal(err)
	}
	// get global framework variables
	f := framework.Global
	// wait for operator to be ready
	err = e2eutil.WaitForDeployment(t, f.KubeClient, namespace, "spp-operator", 1, retryInterval, timeout)
	if err != nil {
		t.Fatal(err)
	}

	if err = sppTest(t, f, ctx); err != nil {
		t.Fatal(err)
	}
}

func sppTest(t *testing.T, f *framework.Framework, ctx *framework.TestCtx) error {
	namespace, err := ctx.GetNamespace()
	if err != nil {
		return fmt.Errorf("could not get namespace: %v", err)
	}
	// create custom resource
	spp := &operator.Spp{
		TypeMeta: metav1.TypeMeta{
			Kind:       "Spp",
			APIVersion: "spp.spp/v1",
		},
		ObjectMeta: metav1.ObjectMeta{
			Name:      "e2e-test",
			Namespace: namespace,
		},
		Spec: operator.SppSpec{
			Ctl: operator.SppCtl{
				Name:  "ctl",
				Image: "sppc/spp-ctl:18.04",
			},
			Primary: operator.SppPrimary{
				Name:  "primary",
				Image: "sppc/spp-ubuntu:18.04",
				Eal: operator.EalOption{
					Lcores:    "1",
					SocketMem: "1024",
				},
				PortMask: "0x07",
			},
		},
	}
	// use TestCtx's create helper to create the object and add a cleanup function for the new object
	err = f.Client.Create(goctx.TODO(), spp, &framework.CleanupOptions{TestContext: ctx, Timeout: cleanupTimeout, RetryInterval: cleanupRetryInterval})
	if err != nil {
		return err
	}

	time.Sleep(timeout)
	pod_ctl := &corev1.Pod{}
	err = f.Client.Get(goctx.TODO(), types.NamespacedName{Name: "e2e-test-ctl-pod", Namespace: namespace}, pod_ctl)
	if err != nil {
		return err
	}
	service_ctl := &corev1.Service{}
	err = f.Client.Get(goctx.TODO(), types.NamespacedName{Name: "e2e-test-ctl-service", Namespace: namespace}, service_ctl)
	if err != nil {
		return err
	}

	time.Sleep(timeout)
	pod_primary := &corev1.Pod{}
	err = f.Client.Get(goctx.TODO(), types.NamespacedName{Name: "e2e-test-primary-pod", Namespace: namespace}, pod_primary)
	if err != nil {
		return err
	}

	url := "http://" + service_ctl.Spec.ClusterIP + ":7777/v1/processes"
	_, err = http.Get(url)
	if err != nil {
		return err
	}

	return nil
}
