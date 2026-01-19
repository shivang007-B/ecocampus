export default function EcoCard({ title, value, icon, children }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-md hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-primary font-semibold text-lg">{title}</h3>
          <p className="text-gray-600 mt-2 text-2xl font-bold">{value}</p>
        </div>
        {icon && <div className="text-4xl">{icon}</div>}
      </div>
      {children && <div className="mt-4">{children}</div>}
    </div>
  );
}