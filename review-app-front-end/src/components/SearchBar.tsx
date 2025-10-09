interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: () => void;
  placeholder?: string;
}

function SearchBar({
  value,
  onChange,
  onSearch,
  placeholder = 'Search...',
}: SearchBarProps) {
  return (
    <div className="p-4 flex justify-center items-center bg-white-900 sticky top-0 z-10">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-indigo-500 w-64"
      />
      <button
        onClick={onSearch}
        className="ml-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500"
      >
        Search
      </button>
    </div>
  );
}

export default SearchBar;
