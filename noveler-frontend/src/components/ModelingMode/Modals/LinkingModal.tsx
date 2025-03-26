import React from 'react';
import useStore from '../../../store/useStore';

const LinkingModal: React.FC = () => {
  const setUIState = useStore((state) => state.setUIState);

  const handleClose = () => {
    setUIState({ showModal: false });
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-4 rounded">
        <h2 className="text-xl mb-4">Linking Modal</h2>
        {/* Add linking form here */}
        <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleClose}>
          Close
        </button>
      </div>
    </div>
  );
};

export default LinkingModal;