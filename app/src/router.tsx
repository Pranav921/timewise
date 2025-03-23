import { createRouter, ErrorComponent } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient();

export const router = createRouter({
  routeTree,
  context: {
    auth: undefined!,
    queryClient,
  },
  defaultPreloadStaleTime: 0, // let react query handle the data loading/caching
  // defaultPendingComponent: () => <p>Loading...</p>,
  // defaultErrorComponent: ({ error }) => <ErrorComponent error={error} />,
});
