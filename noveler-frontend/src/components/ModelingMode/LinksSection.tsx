import React from 'react';
import useStore from '../../store/useStore';

const LinksSection: React.FC = () => {
  const selectedObject = useStore((state) => state.ui.selectedObject);
  const setModelingObjects = useStore((state) => state.setModelingObjects);

  const handleRemoveLink = (linkId: string) => {
    if (!selectedObject) return;

    const updatedLinks = selectedObject.links.filter((link) => link.id !== linkId);
    const updatedObject = { ...selectedObject, links: updatedLinks };

    setModelingObjects(selectedObject.id, updatedObject);
  };

  if (!selectedObject || selectedObject.links.length === 0) {
    return null;
  }

  return (
    <div className="w-1/5 p-4">
      <h2 className="text-xl mb-4">Links</h2>
      <ul>
        {selectedObject.links.map((link) => (
          <li key={link.id} className="flex justify-between items-center">
            <span>{link.id}</span>
            <button
              className="text-red-500"
              onClick={() => handleRemoveLink(link.id)}
            >
              X
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LinksSection;