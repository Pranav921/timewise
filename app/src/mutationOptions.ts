import type { DefaultError } from "@tanstack/query-core";
import type { UseMutationOptions } from "@tanstack/react-query";
import { queryClient } from "./router";
import { DataClient, dataClient } from "./dataClient";
import { overviewInfoQueryOptions } from "./queryOptions";

// https://github.com/TanStack/query/discussions/6096#discussioncomment-9685102
export function mutationOptions<
  TData = unknown,
  TError = DefaultError,
  TVariables = void,
  TContext = unknown,
>(
  options: UseMutationOptions<TData, TError, TVariables, TContext>,
): UseMutationOptions<TData, TError, TVariables, TContext> {
  return options;
}

type FirstArgument<T extends (...args: any) => any> = Parameters<T>[0];

const commonOptions: Omit<
  UseMutationOptions<any, any, any, any>,
  "mutationFn"
> = {
  onError: (error) => {
    console.error(error);
  },
  retry: 3,
};

export const createPlanMutationOptions = mutationOptions({
  mutationFn: (args: FirstArgument<DataClient["createPlan"]>) =>
    dataClient.createPlan(args),
  onSuccess: () => {
    // TODO: update the query cache with the newly created item, instead of invalidating the query to avoid additional requests
    queryClient.invalidateQueries({
      queryKey: overviewInfoQueryOptions.queryKey,
    });
  },
  ...commonOptions,
});

export const editPlanMutationOptions = mutationOptions({
  mutationFn: (args: FirstArgument<DataClient["editPlan"]>) =>
    dataClient.editPlan(args),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: overviewInfoQueryOptions.queryKey,
    });
  },
  ...commonOptions,
});

export const deletePlanMutationOptions = mutationOptions({
  mutationFn: (args: FirstArgument<DataClient["deletePlan"]>) =>
    dataClient.deletePlan(args),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: overviewInfoQueryOptions.queryKey,
    });
  },
  ...commonOptions,
});

export const createScheduleMutationOptions = mutationOptions({
  mutationFn: (args: FirstArgument<DataClient["createSchedule"]>) =>
    dataClient.createSchedule(args),
  onSuccess: () => {
    // TODO: update the query cache with the newly created item, instead of invalidating the query to avoid additional requests
    queryClient.invalidateQueries({
      queryKey: overviewInfoQueryOptions.queryKey,
    });
  },
  ...commonOptions,
});

export const editScheduleMutationOptions = mutationOptions({
  mutationFn: (args: FirstArgument<DataClient["editSchedule"]>) =>
    dataClient.editSchedule(args),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: overviewInfoQueryOptions.queryKey,
    });
  },
  ...commonOptions,
});

export const deleteScheduleMutationOptions = mutationOptions({
  mutationFn: (args: FirstArgument<DataClient["deleteSchedule"]>) =>
    dataClient.deleteSchedule(args),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: overviewInfoQueryOptions.queryKey,
    });
  },
  ...commonOptions,
});
