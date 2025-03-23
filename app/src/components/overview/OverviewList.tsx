import { useState, useRef, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import Button from "../Button";
import Input from "../Input";
import Select from "../Select";
import { ClassSchedule, FourYearPlan } from "../../types";

type Item = FourYearPlan | ClassSchedule;

type OverviewListProps = {
  title: string;
  children?: React.ReactNode;
  data: Item[];

  createItem: (item: Item) => void;
  editItem: (updatedItem: Item) => void;
  deleteItem: (id: string) => void;
};

function OverviewList({
  title,
  data,
  createItem,
  editItem,
  deleteItem,
}: OverviewListProps) {
  const [isCreatingItem, setIsCreatingItem] = useState(false);
  const [itemBeingEdited, setItemBeingEdited] = useState<Item | null>(null);
  const [itemBeingDeleted, setItemBeingDeleted] = useState<Item["id"] | null>(
    null,
  );

  return (
    <div>
      <div className="p-1">
        <div className="flex items-center justify-between p-2 bg-indigo-50 rounded-md">
          <p className="text-base font-semibold text-gray-500">{title}</p>
          <Button
            className="text-sm py-1 px-2"
            onClick={() => setIsCreatingItem(true)}
          >
            + new
          </Button>
        </div>
      </div>
      <div className="mt-1">
        <div className="cursor-pointer">
          {data.map((item) => {
            if (itemBeingEdited && itemBeingEdited.id === item.id) {
              return (
                <EditItem
                  key={item.id}
                  item={itemBeingEdited}
                  editItem={(updatedItem) => {
                    editItem(updatedItem);
                    setItemBeingEdited(null);
                  }}
                  cancelEdit={() => setItemBeingEdited(null)}
                />
              );
            }
            return (
              <OverviewListItem
                key={item.id}
                item={item}
                isDeleting={itemBeingDeleted === item.id}
                onEditItem={(item: Item) => setItemBeingEdited(item)}
                onDeleteItem={(id: string) => setItemBeingDeleted(id)}
                deleteItem={deleteItem}
                cancelDelete={() => setItemBeingDeleted(null)}
              />
            );
          })}
        </div>
        {isCreatingItem && (
          <NewItem
            createItem={(newItem) => {
              createItem(newItem);
              setIsCreatingItem(false);
            }}
            cancelCreate={() => setIsCreatingItem(false)}
          />
        )}
      </div>
    </div>
  );
}

type OverviewListItemProps = {
  item: Item;
  isDeleting: boolean;
  onEditItem: (item: Item) => void;
  onDeleteItem: (id: string) => void;
  deleteItem: (id: string) => void;
  cancelDelete: () => void;
};

function OverviewListItem({
  item,
  isDeleting,
  onEditItem,
  onDeleteItem,
  deleteItem,
  cancelDelete,
}: OverviewListItemProps) {
  const renderActions = () => {
    if (isDeleting) {
      return (
        <div className="delete-confirmation-actions">
          <span
            className="mr-2 rounded-md p-1.5 hover:bg-gray-200"
            onClick={cancelDelete}
          >
            ❌
          </span>
          <span
            className="rounded-md p-1.5 hover:bg-gray-200"
            onClick={() => deleteItem(item.id)}
          >
            ✅
          </span>
        </div>
      );
    }

    return (
      <div>
        <span
          className="mr-2 rounded-md p-1.5 hover:bg-gray-200"
          onClick={(e) => {
            e.stopPropagation();
            onEditItem(item);
          }}
        >
          ✏️
        </span>
        <span
          className="rounded-md p-1.5 hover:bg-red-100"
          onClick={() => onDeleteItem(item.id)}
        >
          🗑️
        </span>
      </div>
    );
  };

  return (
    <div
      onMouseLeave={() => {
        if (isDeleting) cancelDelete();
      }}
      className="group flex p-2 justify-between items-center w-full hover:bg-gray-100 hover:cursor-pointer"
    >
      <div className="flex flex-col w-3/4">
        <p className="truncate">{item.name}</p>
        <p className="text-sm text-gray-500">
          {item.semester} {item.year} | {item.dateCreated}
        </p>
      </div>
      <div className="invisible group-hover:visible select-none">
        {renderActions()}
      </div>
    </div>
  );
}

type NewItemProps = {
  createItem: (newItem: Item) => void;
  cancelCreate: () => void;
};

function NewItem({ createItem: innerCreateItem, cancelCreate }: NewItemProps) {
  const itemNameRef = useRef<string>("Untitled");
  const semesterRef = useRef<string>("Fall");
  const yearRef = useRef<string>("2025");
  const newItemContainerRef = useRef<HTMLDivElement | null>(null);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    itemNameRef.current = e.target.value;
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // e.preventDefault();
    if (e.key === "Enter") {
      createItem();
    }
  };

  const onSemesterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    semesterRef.current = e.target.value;
  };

  const onYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    yearRef.current = e.target.value;
  };

  const createItem = () => {
    const name = itemNameRef.current === "" ? "Untitled" : itemNameRef.current;

    innerCreateItem({
      id: uuidv4(),
      name,
      semester: semesterRef.current,
      year: yearRef.current,
      dateCreated: "3/17/2025",
    });
  };

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        newItemContainerRef.current &&
        !newItemContainerRef.current.contains(e.target as HTMLElement)
      ) {
        createItem();
      }
    }

    function handleKeydown(e: KeyboardEvent) {
      if (e.key === "Enter") {
        createItem();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeydown);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeydown);
    };
  }, []);

  return (
    <div className="min-h-[60px]" ref={newItemContainerRef}>
      <div className="flex items-center p-2 gap-1">
        <div className="flex-1">
          <Input
            placeholder="Enter a name..."
            onChange={onChange}
            onKeyDown={onKeyDown}
            autoFocus
          />
        </div>
        <div>
          <Select onChange={onSemesterChange}>
            <option value="Fall">Fall</option>
            <option value="Spring">Spring</option>
            <option value="Summer">Summer</option>
          </Select>
        </div>
        <div>
          <Select onChange={onYearChange}>
            <option value="2025">2025</option>
            <option value="2026">2026</option>
            <option value="2027">2027</option>
            <option value="2028">2028</option>
          </Select>
        </div>
      </div>
      <div className="flex pl-3">
        <span
          className="text-xs text-red-400 hover:underline pb-2 cursor-pointer"
          onClick={cancelCreate}
        >
          Cancel
        </span>
      </div>
    </div>
  );
}

type EditItemProps = {
  item: Item;
  editItem: (updatedItem: Item) => void;
  cancelEdit: () => void;
};

function EditItem({
  item,
  editItem: innerEditItem,
  cancelEdit,
}: EditItemProps) {
  const itemNameRef = useRef<string>(item.name);
  const semesterRef = useRef<string>(item.semester);
  const yearRef = useRef<string>(item.year);
  const editItemContainerRef = useRef<HTMLDivElement | null>(null);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    itemNameRef.current = e.target.value;
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // e.preventDefault();
    if (e.key === "Enter") {
      editItem();
    }
  };

  const onSemesterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    semesterRef.current = e.target.value;
  };

  const onYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    yearRef.current = e.target.value;
  };

  const editItem = () => {
    const name = itemNameRef.current === "" ? "Untitled" : itemNameRef.current;

    innerEditItem({
      ...item,
      name,
      semester: semesterRef.current,
      year: yearRef.current,
    });
  };

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        editItemContainerRef.current &&
        !editItemContainerRef.current.contains(e.target as HTMLElement)
      ) {
        editItem();
      }
    }

    function handleKeydown(e: KeyboardEvent) {
      if (e.key === "Enter") {
        editItem();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeydown);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeydown);
    };
  }, []);

  return (
    <div className="min-h-[60px]" ref={editItemContainerRef}>
      <div className="flex items-center px-2 gap-1">
        <div className="flex-1">
          <Input
            defaultValue={item.name}
            placeholder="Enter a name..."
            onChange={onChange}
            onKeyDown={onKeyDown}
            autoFocus
          />
        </div>
        <div>
          <Select onChange={onSemesterChange} defaultValue={item.semester}>
            <option value="Fall">Fall</option>
            <option value="Spring">Spring</option>
            <option value="Summer">Summer</option>
          </Select>
        </div>
        <div>
          <Select onChange={onYearChange} defaultValue={item.year}>
            <option value="2025">2025</option>
            <option value="2026">2026</option>
            <option value="2027">2027</option>
            <option value="2028">2028</option>
          </Select>
        </div>
      </div>
      <div className="flex relative pl-3">
        <span
          className="text-xs absolute top-1 text-red-400 hover:underline"
          onClick={cancelEdit}
        >
          Cancel
        </span>
      </div>
    </div>
  );
}

export default OverviewList;
