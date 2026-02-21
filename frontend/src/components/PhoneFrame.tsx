import React from "react";

interface PhoneFrameProps {
  children: React.ReactNode;
}

const PhoneFrame: React.FC<PhoneFrameProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-cream-dark p-4">
      <div
        className="phone-frame relative w-[400px] h-[780px] bg-background rounded-[2.5rem] border-4 border-muted overflow-hidden flex flex-col"
        role="application"
        aria-label="Banking App"
      >
        {/* Status bar */}
        <div className="flex items-center justify-between px-6 pt-3 pb-1">
          <span className="text-sm font-semibold text-foreground">9:41</span>
          <div className="flex gap-1.5 items-center">
            <div className="w-4 h-3 rounded-sm bg-foreground opacity-70" />
            <div className="w-4 h-3 rounded-sm bg-foreground opacity-70" />
            <div className="w-6 h-3 rounded-md bg-primary opacity-80" />
          </div>
        </div>
        {/* App content */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden">
          {children}
        </div>
      </div>
    </div>
  );
};

export default PhoneFrame;
