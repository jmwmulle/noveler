import React, { useEffect, useState } from 'react';
import useStore from '../../store/useStore';

const MenuSection: React.FC = () => {
  const [objectTypes, setObjectTypes] = useState([]);
  const setModelingObjects = useStore((state) => state.setModelingObjects);

  useEffect(() => {
    fetch('/user/routes/builder/object-types')
      .then((response) => response.json())
      .then((data) => setObjectTypes(data));
  }, []);

  const handleObjectTypeClick = (objectType: string) => {
    fetch(`/list/${objectType}`)
      .then((response) => response.json())
      .then((data) => setModelingObjects(objectType, data));
  };

  return (
    <div className="w-1/5 p-4">
      <h2 className="text-xl mb-4">Object Types</h2>
      <ul>
        {objectTypes.map((type) => (
          <li key={type.id}>
            <button
              className="text-blue-500"
              onClick={() => handleObjectTypeClick(type.name)}
            >
              {type.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MenuSection;