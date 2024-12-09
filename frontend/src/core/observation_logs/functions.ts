export const commentShortened = (comment: string | null) => {
    if (comment && comment.length > 255) {
        return comment.substring(0, 255) + "...";
    }
    return comment;
};
