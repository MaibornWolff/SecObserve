import React from "react";

type IntervalCallback = () => void;

// Taken from https://stackoverflow.com/a/70935119

function useDispatch(callback: IntervalCallback, delay: number): void {
    const cachedCallback = React.useRef<IntervalCallback>();

    React.useEffect(() => {
        cachedCallback.current = callback;
    }, [callback]);

    React.useEffect(() => {
        if (delay !== 0) {
            const id = setInterval(() => cachedCallback?.current?.(), delay);
            return () => clearInterval(id);
        }
    }, [delay]);
}

export const IntervalHooks = {
    useDispatch,
};
