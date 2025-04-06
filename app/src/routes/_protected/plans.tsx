import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_protected/plans")({
  component: RouteComponent,
  loader: ({ context }) => {
    console.log("loading plans...");
  },
});

function RouteComponent() {
  return <div>Hello "/_protected/plans"!</div>;
}
