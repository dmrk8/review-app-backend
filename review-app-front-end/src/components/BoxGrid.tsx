import React from 'react';

interface BoxGridProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function BoxGrid<T>({ items, renderItem }: BoxGridProps<T>) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      {items.map((item, index) => (
        <React.Fragment key={index}>{renderItem(item)}</React.Fragment>
      ))}
    </div>
  );
}

export default BoxGrid;
