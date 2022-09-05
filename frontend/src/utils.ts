import { formatDistance } from "date-fns";

export function utcTs() {
    return new Date().getTime();
}
    
export function formatEnd(t) {
    return formatDistance(
        t,
        utcTs(),
        {
            includeSeconds: true
        }
    )
}