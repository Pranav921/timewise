export interface OverviewInfo {
  fourYearPlans: FourYearPlan[];
  classSchedules: ClassSchedule[];
  university: string;
}

export interface FourYearPlan {
  id: string;
  name: string;
  semester: string;
  year: string;
  dateCreated: string;
}

export interface ClassSchedule {
  id: string;
  name: string;
  semester: string;
  year: string;
  dateCreated: string;
}
