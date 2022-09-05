import { formatDistance } from "date-fns";

function utc_ts() {
    return new Date().getTime();
}
    
export function formatEnd(t) {
    return formatDistance(
        t,
        utc_ts(),
        {
            includeSeconds: true
        }
    )
}