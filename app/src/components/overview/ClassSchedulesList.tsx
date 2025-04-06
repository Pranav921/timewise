import { useMutation } from "@tanstack/react-query";
import OverviewList from "./OverviewList";
import { ClassSchedule } from "../../types";
import {
  createScheduleMutationOptions,
  deleteScheduleMutationOptions,
  editScheduleMutationOptions,
} from "../../mutationOptions";

type ClassSchedulesListProps = {
  data: ClassSchedule[];
  selectItem: (id: string) => void;
};

function ClassSchedulesList({ data, selectItem }: ClassSchedulesListProps) {
  const createScheduleMutation = useMutation({
    ...createScheduleMutationOptions,
    onError: (e) => {
      console.log("ERRRRRORR", e);
    },
  });
  const editScheduleMutation = useMutation(editScheduleMutationOptions);
  const deleteScheduleMutation = useMutation(deleteScheduleMutationOptions);

  const createItem = (newItem: ClassSchedule) => {
    createScheduleMutation.mutate({
      name: newItem.name,
      semester: newItem.semester,
    });
  };

  const editItem = (newItem: ClassSchedule) => {
    editScheduleMutation.mutate(newItem);
  };

  const deleteItem = (id: string) => {
    deleteScheduleMutation.mutate(id);
  };

  return (
    <OverviewList
      title="Class Schedules"
      onClickItem={selectItem}
      createItem={createItem}
      editItem={editItem}
      deleteItem={deleteItem}
      data={data}
    />
  );
}

export default ClassSchedulesList;
