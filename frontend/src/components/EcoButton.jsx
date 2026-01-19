export default function EcoButton({ children, variant = "primary", ...props }) {
  const baseStyles = "px-6 py-2 rounded-xl font-medium transition-all duration-300";
  
  const variants = {
    primary: "bg-primary text-white hover:bg-secondary hover:shadow-lg",
    secondary: "bg-secondary text-white hover:bg-primary hover:shadow-lg",
    outline: "border-2 border-primary text-primary hover:bg-primary hover:text-white",
  };

  return (
    <button className={`${baseStyles} ${variants[variant]}`} {...props}>
      {children}
    </button>
  );
}