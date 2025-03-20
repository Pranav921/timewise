import { useState } from "react";

import OverviewList from "./OverviewList";
import { v4 as uuidv4 } from "uuid";
import { FourYearPlan } from "../../types";

// TODO:
// create fetching client, ensure that it is flexible to handle guest mode + logged in
// start working on four year plans views, at least have it show a four year plan
// start working on the calendar to show class calendar

type FourYearPlansListProps = {
  data: FourYearPlan[];
};

function FourYearPlansList({ data }: FourYearPlansListProps) {
  const [items, setItems] = useState([
    {
      id: uuidv4(),
      name: "My four year plan",
      semester: "Spring",
      year: "2025",
      dateCreated: "3/17/2025",
    },
    {
      id: uuidv4(),
      name: "My four year plan",
      semester: "Spring",
      year: "2025",
      dateCreated: "3/17/2025",
    },
    {
      id: uuidv4(),
      name: "My four year plan",
      semester: "Spring",
      year: "2025",
      dateCreated: "3/17/2025",
    },
  ]);

  const createItem = (newItem: FourYearPlan) => {
    setItems((prev) => [...prev, newItem]);
  };

  const editItem = (newItem: FourYearPlan) => {
    setItems((prev) =>
      prev.map((item) => {
        if (item.id === newItem.id) {
          return {
            ...item,
            ...newItem,
          };
        }
        return item;
      }),
    );
  };

  const deleteItem = (id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  };

  return (
    <OverviewList
      title="4-Year Plans"
      createItem={createItem}
      editItem={editItem}
      deleteItem={deleteItem}
      data={data}
    />
  );
}
export default FourYearPlansList;
