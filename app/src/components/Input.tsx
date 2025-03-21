// https://react-typescript-cheatsheet.netlify.app/docs/advanced/patterns_by_usecase/
export interface InputProps extends React.ComponentPropsWithRef<"input"> {
  icon?: React.ReactNode;
}

const inputClass = `block w-full py-1.5 px-2 focus:outline-none`;

function Input(props: InputProps) {
  const { className, icon, ref, ...rest } = props;

  return (
    <div
      className={`flex items-center rounded-md outline-1 
      outline-gray-200 -outline-offset-1 focus-within:outline-2 
        focus-within:-outline-offset-2 focus-within:outline-gray-300 ${className}`}
    >
      {icon && <div className="pl-2">{icon}</div>}
      <input {...rest} className={`${inputClass}`} ref={ref} />
    </div>
  );
}

export default Input;
