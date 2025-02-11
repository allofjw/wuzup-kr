export async function fetchJsonData<T>(endpoint: string): Promise<T> {
    try {
      console.log("Fetching from " + endpoint);
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data: T = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching JSON data:", error);
      throw error;
    }
  }