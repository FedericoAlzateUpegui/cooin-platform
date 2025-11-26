/**
 * Error handling utilities
 */

/**
 * Type guard to check if value is an Error object
 */
export function isError(error: unknown): error is Error {
  return error instanceof Error;
}

/**
 * Type guard to check if error has a message property
 */
export function hasMessage(error: unknown): error is { message: string } {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    typeof (error as { message: unknown }).message === 'string'
  );
}

/**
 * Type guard to check if error has a detail property
 */
export function hasDetail(error: unknown): error is { detail: string } {
  return (
    typeof error === 'object' &&
    error !== null &&
    'detail' in error &&
    typeof (error as { detail: unknown }).detail === 'string'
  );
}

/**
 * Type guard for axios-like errors with response property
 */
export function hasResponse(
  error: unknown
): error is { response: { data?: { detail?: string; error?: { message?: string } }; status?: number } } {
  return (
    typeof error === 'object' &&
    error !== null &&
    'response' in error &&
    typeof (error as { response: unknown }).response === 'object'
  );
}

/**
 * Extract error message from unknown error type
 */
export function getErrorMessage(error: unknown): string {
  if (hasResponse(error)) {
    return (
      error.response?.data?.detail ||
      error.response?.data?.error?.message ||
      'An error occurred'
    );
  }

  if (hasDetail(error)) {
    return error.detail;
  }

  if (hasMessage(error)) {
    return error.message;
  }

  if (isError(error)) {
    return error.message;
  }

  if (typeof error === 'string') {
    return error;
  }

  return 'An unknown error occurred';
}

/**
 * Get error details for logging
 */
export function getErrorDetails(error: unknown): {
  message: string;
  response?: unknown;
  status?: number;
} {
  const details: { message: string; response?: unknown; status?: number } = {
    message: getErrorMessage(error),
  };

  if (hasResponse(error)) {
    details.response = error.response?.data;
    details.status = error.response?.status;
  }

  return details;
}
