export interface LibraryReviewType {
    review_id: string;
    media_id: number;

    review?: string;
    rating?: number;
    created_at: string;  // Use string for Date in JSON
    updated_at: string;
    
    title?: string;
    description?: string;
    start_year?: number;
    end_year?: number;
    type: string;
    cover_image?: string;

}