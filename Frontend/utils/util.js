import { useRouter } from "next/router";

export function useAsset(path) {
  const { basePath } = useRouter();
  return `${basePath}${path}`;
}
