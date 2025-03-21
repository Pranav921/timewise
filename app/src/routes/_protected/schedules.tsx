import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_protected/schedules")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/_protected/schedules"!</div>;
}
