import { useMutation } from "@tanstack/react-query";
import OverviewList from "./OverviewList";
import { FourYearPlan } from "../../types";
import {
  createPlanMutationOptions,
  deletePlanMutationOptions,
  editPlanMutationOptions,
} from "../../mutationOptions";

// TODO:
// create fetching client, ensure that it is flexible to handle guest mode + logged in
// start working on four year plans views, at least have it show a four year plan
// start working on the calendar to show class calendar

type FourYearPlansListProps = {
  data: FourYearPlan[];
  selectItem: (id: string) => void;
};

function FourYearPlansList({ data, selectItem }: FourYearPlansListProps) {
  const createPlanMutation = useMutation({
    ...createPlanMutationOptions,
    onError: (e) => {
      console.log("ERRRRRORR", e);
    },
  });
  const editPlanMutation = useMutation(editPlanMutationOptions);
  const deletePlanMutation = useMutation(deletePlanMutationOptions);

  const createItem = async (newItem: FourYearPlan) => {
    createPlanMutation.mutate({
      name: newItem.name,
      semester: newItem.semester,
    });
  };

  const editItem = (newItem: FourYearPlan) => {
    editPlanMutation.mutate(newItem);
  };

  const deleteItem = (id: string) => {
    deletePlanMutation.mutate(id);
  };

  return (
    <OverviewList
      title="4-Year Plans"
      onClickItem={selectItem}
      createItem={createItem}
      editItem={editItem}
      deleteItem={deleteItem}
      data={data}
    />
  );
}

export default FourYearPlansList;
