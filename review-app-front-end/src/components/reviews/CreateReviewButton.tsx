import { useState } from 'react';
import CreateReviewForm from './CreateReviewForm';

interface CreateReviewButtonProps {
  mediaType: string;
  mediaId: number;
  title: string;
  onCreated?: () => void;
}

export default function CreateReviewButton({
  mediaType,
  mediaId,
  title,
  onCreated,
}: CreateReviewButtonProps) {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <button onClick={() => setShowModal(true)}>Create Review</button>
      {showModal && (
        <CreateReviewForm
          mediaType={mediaType}
          mediaId={mediaId}
          title={title}
          onCreated={onCreated}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}
