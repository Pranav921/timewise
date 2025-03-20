import { queryOptions } from "@tanstack/react-query";
import { dataClient } from "./dataClient";

export const overviewInfoQueryOptions = queryOptions({
  queryKey: ["overviewInfo"],
  queryFn: () => dataClient.getOverviewInfo(),
  staleTime: 3000,
});
