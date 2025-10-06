import { useEffect } from "react";

interface UseInfiniteScrollProps {
    callback: () => void;
    isLoading: boolean;
    hasNextPage: boolean;
}

export function UseInfiniteScroll({ callback, isLoading, hasNextPage} : UseInfiniteScrollProps) {
    useEffect(() => {
      if (isLoading || !hasNextPage) return;
      const handleScroll = () => {
        if (
            window.innerHeight + window.scrollY >= document.body.offsetHeight - 200 &&
            !isLoading &&
            hasNextPage
            
        ) {
            callback();
        }
      };
      
      window.addEventListener("scroll", handleScroll);
      return () => {
        window.removeEventListener("scroll", handleScroll);
      }
    }, [callback, isLoading, hasNextPage])    
}