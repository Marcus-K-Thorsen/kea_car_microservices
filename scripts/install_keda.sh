# Check if KEDA is installed
if ! kubectl get namespace keda &> /dev/null; then
  echo "⚠️ KEDA is not installed. Installing KEDA..."
  kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.16.1/keda-2.16.1.yaml

  # Wait for KEDA to be ready
  echo "Waiting for KEDA to be ready..."
  kubectl wait --for=condition=available --timeout=600s deployment/keda-operator -n keda
else
  echo "✅ KEDA is already installed."
fi