import React from 'react';
import useStore from '../../store/useStore';

const ListSection: React.FC = () => {
  const modeling = useStore((state) => state.modeling);
  const selectedObjectType = Object.keys(modeling)[0];
  const objects = modeling[selectedObjectType] || [];

  return (
    <div className="w-1/5 p-4">
      <h2 className="text-xl mb-4">Objects</h2>
      <ul>
        {objects.map((obj) => (
          <li key={obj.id}>{obj.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default ListSection;