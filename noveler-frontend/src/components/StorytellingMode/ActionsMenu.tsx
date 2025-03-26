import React from 'react';
import useStore from '../../store/useStore';

const ActionsMenu: React.FC = () => {
  const selectedStory = useStore((state) => state.ui.selectedStory);
  const setUIState = useStore((state) => state.setUIState);

  const handleAnnotate = () => {
    setUIState({ modalType: 'annotation', showModal: true });
  };

  if (!selectedStory) {
    return null;
  }

  return (
    <div className="p-4">
      <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={handleAnnotate}>
        Annotate
      </button>
    </div>
  );
};

export default ActionsMenu;