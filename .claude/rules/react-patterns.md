---
paths: "**/*.jsx,**/*.js,**/*.tsx,**/*.ts"
---

# React & JavaScript/TypeScript Rules

## File Extensions (grupo-lawteck uses JS, NOT TypeScript)

| Type | Extension | Export | Example |
|------|-----------|--------|---------|
| Components | `.jsx` | `export default function Name()` | `BoardList.jsx` |
| Hooks | `.js` | `export function useName()` | `useBoardList.js` |
| Services | `.js` | `export const nameService = {}` | `stockService.js` |
| Contexts | `.jsx` | `export const useCtx = () => useContext(Ctx)` | `AuthContext.jsx` |
| Utils | `.js` | Named exports | `utils.js` |

## Component Structure

- Functional components only (no classes)
- Default export for components
- Props destructured in function signature: `function Card({ title, onEdit }) {}`
- Use `cn()` from `lib/utils` for className merging (clsx + tailwind-merge)
- Styling: TailwindCSS utility classes only, no CSS files
- Icons: `lucide-react` library

## Custom Hooks Pattern

- Location: `src/hooks/useXxx.js`
- Named export: `export function useXxx() {}`
- Return plain object with all state + handlers
- Use `useCallback` for memoized handlers with complete dependency arrays
- Multiple `useState` grouped by logical concern

## Service Layer

- Location: `src/services/xxxService.js`
- Plain objects with async methods (NOT classes)
- Pattern: `const { data, error } = await supabase.from(...); if (error) throw error;`
- Let calling code handle errors via try/catch

## Context Pattern

- Always export both Provider and a `useXxx` convenience hook
- Disable refresh warnings: `/* eslint-disable react-refresh/only-export-components */`

## Error Handling

- Use `parseErrorMessage(error)` from `hooks/useFormErrors.js` for user-friendly messages
- Show errors via `useToast()` from `ToastContext`
- Capture exceptions: `captureException()` from error tracker

## UI Library

- Radix UI primitives + custom wrappers in `src/components/UI/`
- Always use existing UI components before creating new ones
- Follow `forwardRef` pattern for compound components

## State Management

- React Context + local state (no Redux/Zustand)
- Heavy hooks: extract to `src/hooks/useXxx.js`
- Keep hooks focused: one hook per feature/page concern

## Imports

- Relative imports (no `@/` path aliases configured)
- Environment: `import.meta.env.VITE_*` for Vite variables
- Group: React → third-party → local components → local hooks → local utils

## Language

- UI text and error messages in Portuguese (pt-BR)
- Variable names and code comments in English
- No i18n library — hardcoded strings
