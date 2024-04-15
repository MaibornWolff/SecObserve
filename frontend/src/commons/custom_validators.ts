import { maxLength, maxValue, minValue, required } from "react-admin";

export const validate_required = [required()];
export const validate_required_150 = [required(), maxLength(150)];
export const validate_required_255 = [required(), maxLength(255)];
export const validate_150 = [maxLength(150)];
export const validate_255 = [maxLength(255)];
export const validate_513 = [maxLength(513)];
export const validate_2048 = [maxLength(2048)];

export const validate_0_10 = [minValue(0), maxValue(10)];
export const validate_0_999999 = [minValue(0), maxValue(999999)];
