import CreateReviewButton from './reviews/CreateReviewButton';
import type { MediaType } from '../types/Media';

interface MediaModalProps {
  media: MediaType | null;
  onClose: () => void;
}

function MediaModal({ media, onClose }: MediaModalProps) {
  if (!media) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-50">
      <div className="bg-gray-900 text-white rounded-2xl max-w-md w-full p-6 relative shadow-2xl">
        <button
          className="absolute top-4 right-4 text-gray-400 hover:text-white"
          onClick={onClose}
          aria-label="Close modal"
        >
          ✕
        </button>
        {media.cover_image && (
          <img
            src={media.cover_image}
            alt={media.title}
            className="w-full h-64 object-cover rounded-xl mb-4"
          />
        )}
        <h3 className="text-xl font-bold mb-2">{media.title}</h3>
        <p className="mb-2">{media.description}</p>
        <p className="text-gray-400 text-sm mb-4">
          {media.start_year} - {media.end_year || 'Ongoing'}
        </p>
        <div className="flex gap-2">
          <CreateReviewButton
            mediaType={media.type}
            mediaId={media.media_id}
            title={media.title}
          />
          <button
            className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default MediaModal;
