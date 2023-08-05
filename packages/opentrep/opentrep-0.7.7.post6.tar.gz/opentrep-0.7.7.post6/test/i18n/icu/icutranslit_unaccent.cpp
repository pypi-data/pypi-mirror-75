/********************************************************************
 * COPYRIGHT:
 * Copyright (c) 1999-2003, International Business Machines Corporation and
 * others. All Rights Reserved.
 ********************************************************************/
// ICU
#include "icutranslit_unaccent.hpp"

const char UnaccentTransliterator::fgClassID = 0;

/**
 * Constructor
 */
UnaccentTransliterator::UnaccentTransliterator() :
  Transliterator ("Unaccent", 0),
  normalizer ("", UNORM_NFD) {
}

/**
 * Destructor
 */
UnaccentTransliterator::~UnaccentTransliterator() {
}

/**
 * Remove accents from a character using Normalizer.
 */
UChar UnaccentTransliterator::unaccent(UChar c) const {
    UnicodeString str(c);
    UErrorCode status = U_ZERO_ERROR;
    UnaccentTransliterator* t = (UnaccentTransliterator*)this;

    t->normalizer.setText(str, status);
    if (U_FAILURE(status)) {
        return c;
    }
    return (UChar) t->normalizer.next();
}

/**
 * Implement Transliterator API
 */
void UnaccentTransliterator::handleTransliterate(Replaceable& text,
                                                 UTransPosition& index,
                                                 UBool incremental) const {
    UnicodeString str("a");
    while (index.start < index.limit) {
        UChar c = text.charAt(index.start);
        UChar d = unaccent(c);
        if (c != d) {
            str.setCharAt(0, d);
            text.handleReplaceBetween(index.start, index.start+1, str);
        }
        index.start++;
    }
}
