import { useState } from "react";

import OverviewList from "./OverviewList";
import { v4 as uuidv4 } from "uuid";
import { ClassSchedule } from "../../types";

type ClassSchedulesListProps = {
  data: ClassSchedule[];
};

function ClassSchedulesList({ data }: ClassSchedulesListProps) {
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

  const createItem = (newItem: ClassSchedule) => {
    setItems((prev) => [...prev, newItem]);
  };

  const editItem = (newItem: ClassSchedule) => {
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
      title="Class Schedules"
      createItem={createItem}
      editItem={editItem}
      deleteItem={deleteItem}
      data={data}
    />
  );
}

export default ClassSchedulesList;
