import { OverviewInfo, FourYearPlan, ClassSchedule } from "./types";
import axios from "axios";

// TODO: create a new data client, separate user's log in status and token into a different implementation
export class DataClient {
  private loggedIn = false;
  public token: string | undefined;

  public setLoggedInStatus(loggedIn: boolean): void {
    this.loggedIn = loggedIn;
  }

  public setToken(token: string | undefined) {
    // console.log("setting token: ", token);
    this.token = token;
  }

  public async getPlans(): Promise<FourYearPlan[]> {
    return await axios.get("http://127.0.0.1:8000/api/plans", {
      headers: {
        Authorization: `Bearer ${this.token}`,
        "Content-Type": "application/json",
      },
    });
  }

  public async createPlan(data: Omit<FourYearPlan, "id" | "date">) {
    return await axios.post("http://127.0.0.1:8000/api/plans/create", data, {
      headers: {
        Authorization: `Bearer ${this.token}`,
        "Content-Type": "application/json",
      },
    });
  }

  public async editPlan(newPlan: FourYearPlan) {
    return await axios.post(
      "http://127.0.0.1:8000/api/plans/edit",
      { ...newPlan },
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
          "Content-Type": "application/json",
        },
      },
    );
  }

  public async deletePlan(planId: string) {
    return await axios.post(
      "http://127.0.0.1:8000/api/plans/delete",
      { id: planId },
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
          "Content-Type": "application/json",
        },
      },
    );
  }

  public async createSchedule({
    name,
    semester,
  }: Omit<ClassSchedule, "id" | "date">) {
    return await axios.post(
      "http://127.0.0.1:8000/api/schedules/create",
      { name, semester },
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
          "Content-Type": "application/json",
        },
      },
    );
  }

  public async editSchedule(newSchedule: ClassSchedule) {
    return await axios.post(
      "http://127.0.0.1:8000/api/schedules/edit",
      { ...newSchedule },
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
          "Content-Type": "application/json",
        },
      },
    );
  }

  public async deleteSchedule(scheduleId: string) {
    return await axios.post(
      "http://127.0.0.1:8000/api/schedules/delete",
      {
        id: scheduleId,
      },
      {
        headers: {
          Authorization: `Bearer ${this.token}`,
          "Content-Type": "application/json",
        },
      },
    );
  }

  public async getOverviewInfo(): Promise<OverviewInfo> {
    return (
      await axios.get("http://127.0.0.1:8000/api/overview", {
        headers: {
          Authorization: `Bearer ${this.token}`,
          "Content-Type": "application/json",
        },
      })
    ).data;
  }
}

export const dataClient = new DataClient();
