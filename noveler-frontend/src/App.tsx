import React from 'react';
import AppRoutes from './routes';
import useStore from './store/useStore';
import LinkingModal from './components/ModelingMode/Modals/LinkingModal';
import DeleteModal from './components/ModelingMode/Modals/DeleteModal';
import ErrorModal from './components/ModelingMode/Modals/ErrorModal';
import AnnotationModal from './components/StorytellingMode/AnnotationModal';

const App = () => {
  const { showModal, modalType } = useStore((state) => state.ui);

  return (
    <div className="App">
      <AppRoutes />
      {showModal && modalType === 'linking' && <LinkingModal />}
      {showModal && modalType === 'delete' && <DeleteModal />}
      {showModal && modalType === 'error' && <ErrorModal />}
      {showModal && modalType === 'annotation' && <AnnotationModal />}
    </div>
  );
};

export default App;
