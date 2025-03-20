export interface SelectProps extends React.ComponentPropsWithRef<"select"> {}

const selectClass = `block w-full py-1.5 px-2 focus:outline-none`;

function Select(props: SelectProps) {
  const { className, ref, children, ...rest } = props;

  return (
    <div
      className={`flex items-center rounded-md outline-1 
        outline-gray-200 -outline-offset-1 focus-within:outline-2 
          focus-within:-outline-offset-2 focus-within:outline-gray-300 ${className}`}
    >
      <select {...rest} className={`${selectClass}`} ref={ref}>
        {children}
      </select>
    </div>
  );
}

export default Select;
