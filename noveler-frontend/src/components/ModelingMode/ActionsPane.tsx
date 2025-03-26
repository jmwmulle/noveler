import React from 'react';
import useStore from '../../store/useStore';

const ActionsPane: React.FC = () => {
  const selectedObject = useStore((state) => state.ui.selectedObject);
  const setUIState = useStore((state) => state.setUIState);

  const handleUpdate = () => {
    setUIState({ modalType: 'update', showModal: true });
  };

  const handleInherit = () => {
    setUIState({ modalType: 'inherit', showModal: true });
  };

  const handleClone = () => {
    setUIState({ modalType: 'clone', showModal: true });
  };

  const handleDelete = () => {
    setUIState({ modalType: 'delete', showModal: true });
  };

  if (!selectedObject) {
    return null;
  }

  return (
    <div className="w-1/5 p-4">
      <h2 className="text-xl mb-4">Actions</h2>
      <button className="bg-blue-500 text-white px-4 py-2 rounded mb-2" onClick={handleUpdate}>
        Update
      </button>
      <button className="bg-green-500 text-white px-4 py-2 rounded mb-2" onClick={handleInherit}>
        Inherit
      </button>
      <button className="bg-yellow-500 text-white px-4 py-2 rounded mb-2" onClick={handleClone}>
        Clone
      </button>
      <button className="bg-red-500 text-white px-4 py-2 rounded" onClick={handleDelete}>
        Delete
      </button>
    </div>
  );
};

export default ActionsPane;