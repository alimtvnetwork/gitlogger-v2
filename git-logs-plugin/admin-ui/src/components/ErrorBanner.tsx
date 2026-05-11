export function ErrorBanner({ message }: { message: string }) {
  return (
    <div role="alert" className="gl-banner gl-banner-err">
      <strong>Error.</strong> {message}
    </div>
  );
}
