import React from 'react';
import useStore from '../../../store/useStore';

const DeleteModal: React.FC = () => {
  const selectedObject = useStore((state) => state.ui.selectedObject);
  const setModelingObjects = useStore((state) => state.setModelingObjects);
  const setUIState = useStore((state) => state.setUIState);

  const handleDelete = () => {
    if (!selectedObject) return;

    fetch(`/delete/${selectedObject.id}`, { method: 'DELETE' })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          setModelingObjects(selectedObject.id, []);
          setUIState({ showModal: false });
        } else {
          // Handle error
        }
      });
  };

  const handleClose = () => {
    setUIState({ showModal: false });
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-4 rounded">
        <h2 className="text-xl mb-4">Delete Modal</h2>
        <p>Are you sure you want to delete this object?</p>
        <div className="flex space-x-4 mt-4">
          <button className="bg-red-500 text-white px-4 py-2 rounded" onClick={handleDelete}>
            Delete
          </button>
          <button className="bg-gray-500 text-white px-4 py-2 rounded" onClick={handleClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteModal;