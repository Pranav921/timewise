import { useEffect, useState } from "react";
import { createFileRoute, useRouter } from "@tanstack/react-router";
import {
  useSuspenseQuery,
  useQueryErrorResetBoundary,
} from "@tanstack/react-query";
import FourYearPlansList from "../../components/overview/FourYearPlansList";
import ClassSchedulesList from "../../components/overview/ClassSchedulesList";
import Calendar from "../../components/overview/Calendar";
import { overviewInfoQueryOptions } from "../../queryOptions";
import TimewiseModal from "../../components/Modal";
import FourYearPlanDetails from "../../components/FourYearPlanDetails";
import ScheduleDetails from "../../components/ScheduleDetails";

export const Route = createFileRoute("/_protected/overview")({
  loader: async ({ context }) => {
    const user = await context.auth.authPromise.current!.promise;

    if (user) {
      context.queryClient.ensureQueryData(overviewInfoQueryOptions);
    }
  },
  component: RouteComponent,
  pendingComponent: () => <p>Loading...</p>,
  errorComponent: OverviewError,
});

function RouteComponent() {
  return (
    <div className="w-full">
      <OverviewHeader />
      <OverviewItemsContainer />
    </div>
  );
}

function OverviewHeader() {
  const university = useSuspenseQuery({
    ...overviewInfoQueryOptions,
    select: (data) => data.university,
  });

  return (
    <div className="flex items-start justify-between">
      <div className="overview-header-left">
        <p className="text-xl">Overview</p>
        <p className="text-gray-500">
          Major: Computer Science
          <span className="px-3">|</span>
          Year: 2nd
        </p>
      </div>
      <div className="overview-header-right">
        <p>{university.data}</p>
        <p className="text-right opacity-55">Spring 2025</p>
      </div>
    </div>
  );
}

function OverviewItemsContainer() {
  const [planSelected, setPlanSelected] = useState<string | null>(null); // the id of the selected plan
  const [scheduleSelected, setScheduleSelected] = useState<string | null>(null);
  // i don't know if this is good practice or not
  const { data } = useSuspenseQuery({
    ...overviewInfoQueryOptions,
    select: (data) => ({
      plans: data.plans,
      schedules: data.schedules,
    }),
  });

  return (
    <div className="flex mt-6 justify-between gap-5 w-full">
      <OverviewItem>
        <FourYearPlansList
          data={data.plans}
          selectItem={(id) => setPlanSelected(id)}
        />
      </OverviewItem>
      <OverviewItem>
        <ClassSchedulesList
          data={data.schedules}
          selectItem={(id) => setScheduleSelected(id)}
        />
      </OverviewItem>
      <OverviewItem>
        <Calendar />
      </OverviewItem>

      <TimewiseModal
        isOpen={!!planSelected || !!scheduleSelected}
        onRequestClose={() => {
          setPlanSelected(null);
          setScheduleSelected(null);
        }}
      >
        {!!planSelected && <FourYearPlanDetails id={planSelected} />}
        {!!scheduleSelected && <ScheduleDetails id={scheduleSelected} />}
      </TimewiseModal>
    </div>
  );
}

type OverviewItemProps = {
  children?: React.ReactNode;
};

function OverviewItem({ children }: OverviewItemProps) {
  return (
    <div className="w-full h-full border-1 border-gray-200 rounded-md overflow-hidden">
      {children}
    </div>
  );
}

function OverviewError({ error }: { error: Error; reset: () => void }) {
  const router = useRouter();
  const queryErrorResetBoundary = useQueryErrorResetBoundary();

  useEffect(() => {
    // Reset the query error boundary
    queryErrorResetBoundary.reset();
  }, [queryErrorResetBoundary]);

  return (
    <div>
      {error.message}
      <button
        onClick={() => {
          // Invalidate the route to reload the loader, and reset any router error boundaries
          router.invalidate();
        }}
      >
        retry
      </button>
    </div>
  );
}
