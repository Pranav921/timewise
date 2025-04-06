export interface OverviewInfo {
  plans: FourYearPlan[];
  schedules: ClassSchedule[];
  university: string;
}

export interface FourYearPlan {
  id: string;
  name: string;
  semester: string;
  date?: string;
}

export interface ClassSchedule {
  id: string;
  name: string;
  semester: string;
  date?: string;
}
