import React, { useState } from 'react';
import useStore from '../../store/useStore';

const UserInputComponent: React.FC = () => {
  const [input, setInput] = useState('');
  const selectedStory = useStore((state) => state.ui.selectedStory);
  const setStories = useStore((state) => state.setStories);

  const handleSubmit = () => {
    if (!selectedStory) return;

    const newEntry = {
      id: Date.now().toString(),
      text: input,
      branchPoint: false,
      children: [],
    };

    const updatedEntries = [...selectedStory.entries, newEntry];
    const updatedStory = { ...selectedStory, entries: updatedEntries };

    setStories(selectedStory.id, updatedStory);
    setInput('');

    fetch(`/story/${selectedStory.id}/add-entry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newEntry),
    }).then((response) => response.json());
  };

  return (
    <div className="p-4">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded mb-2"
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
};

export default UserInputComponent;