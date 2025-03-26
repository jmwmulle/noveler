import React, { useState } from 'react';
import useStore from '../../store/useStore';

const EditorPane: React.FC = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const selectedObject = useStore((state) => state.ui.selectedObject);
  const setModelingObjects = useStore((state) => state.setModelingObjects);

  const handleSubmit = () => {
    const objectType = 'yourObjectType'; // Replace with actual object type
    const url = selectedObject
      ? `/update/${objectType}/${selectedObject.id}`
      : `/create/${objectType}`;
    const method = selectedObject ? 'PUT' : 'POST';
    const body = JSON.stringify({ name, description });

    fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          setModelingObjects(objectType, data.data);
        } else {
          // Handle error
        }
      });
  };

  return (
    <div className="w-2/5 p-4">
      <h2 className="text-xl mb-4">Editor</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Submit
        </button>
      </form>
    </div>
  );
};

export default EditorPane;