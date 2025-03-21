import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";
import { DayPicker } from "react-day-picker";

function Calendar() {
  const [selected, setSelected] = useState<Date>();

  return (
    <div className="flex flex-col justify-center">
      <div className="p-1">
        <p className="text-base font-semibold text-gray-500 bg-indigo-50 p-2 rounded-md">
          Calendar
        </p>
      </div>
      <div className="p-2">
        <DayPicker
          className="w-full"
          classNames={{
            today: `text-orange-500`,
            selected: `rounded-md bg-blue-500 text-white`, // Highlight the selected day
          }}
          components={{
            NextMonthButton: ({ className, ...props }) => (
              <button className={className} {...props}>
                <ChevronRight className={`h-7 w-7`} />
              </button>
            ),
            PreviousMonthButton: ({ className, ...props }) => (
              <button className={className} {...props}>
                <ChevronLeft className={`h-7 w-7`} />
              </button>
            ),
          }}
          animate
          mode="single"
          selected={selected}
          onSelect={setSelected}
        />
      </div>
    </div>
  );
}

export default Calendar;
