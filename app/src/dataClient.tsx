import { v4 as uuidv4 } from "uuid";
import { OverviewInfo } from "./types";

class DataClient {
  private loggedIn = false;

  public setLoggedInStatus(loggedIn: boolean): void {
    this.loggedIn = loggedIn;
  }

  public getOverviewInfo(): Promise<OverviewInfo> {
    return this.loggedIn
      ? this.getOverviewInfoAuth()
      : this.getOverviewInfoGuest();
  }

  private getOverviewInfoGuest(): ReturnType<typeof this.getOverviewInfo> {
    throw new Error("TODO");
  }

  private getOverviewInfoAuth(): ReturnType<typeof this.getOverviewInfo> {
    return Promise.resolve({
      fourYearPlans: [
        {
          id: uuidv4(),
          name: "My four year plan",
          semester: "Spring",
          year: "2025",
          dateCreated: "3/17/2025",
        },
      ],

      classSchedules: [
        {
          id: uuidv4(),
          name: "My class schedule",
          semester: "Spring",
          year: "2025",
          dateCreated: "3/17/2025",
        },
      ],

      university: "University of Florida",
    });
  }

  public getAllFourYearPlans() {}
  private getAllFourYearPlansGuest() {}
  private getAllFourYearPlansAuth() {}

  public getFourYearPlan() {}
  private getFourYearPlanGuest() {}
  private getFourYearPlanAuth() {}

  public getAllClassSchedules() {}
  private getAllClassSchedulesGuest() {}
  private getAllClassSchedulesAuth() {}

  public getClassSchedule() {}
  private getClassScheduleGuest() {}
  private getClassScheduleAuth() {}
}

export const dataClient = new DataClient();
