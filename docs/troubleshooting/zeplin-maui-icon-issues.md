# Zeplin-to-MAUI Icon Rendering Issues

Troubleshooting guide for icon rendering problems in `/zeplin-to-maui` generated XAML components.

## Common Issues

### 1. Icons Display as Chinese Characters

**Symptom**: Icons render as Chinese characters (e.g., 嘒, 󰢱) instead of Material Design icons.

**Root Cause**: Incorrect Unicode escape format in XAML Glyph attribute.

**Example**:
```xml
<!-- BROKEN: Icons display as Chinese characters -->
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xe5d2;"
                 Color="White"
                 Size="34" />
```

**Solution**:
```xml
<!-- FIXED: Capital hex digits in XAML format -->
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xE5D2;"
                 Color="White"
                 Size="34" />
```

**Automatic Fix**: The icon converter now automatically converts lowercase HTML entities to uppercase XAML format. Re-run `/zeplin-to-maui` to regenerate components with correct icon codes.

**Manual Fix**: If you have already generated XAML:
1. Find all `Glyph="&#x[lowercase-hex];"` patterns
2. Convert hex digits to uppercase: `&#xe5d2;` → `&#xE5D2;`
3. Or use direct Unicode characters (recommended)

---

### 2. Icons Don't Render at All

**Symptom**: Icons are invisible or show as empty boxes.

**Root Cause**: Missing Material Design Icons font file or incorrect FontFamily reference.

**Verification Steps**:

1. **Check font file exists**:
   ```bash
   # Font file should be in Resources/Fonts/
   ls -la Resources/Fonts/MaterialIcons-Regular.ttf
   ```

2. **Verify MauiProgram.cs configuration**:
   ```csharp
   .ConfigureFonts(fonts =>
   {
       fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
       fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
       fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons"); // ← Required
   });
   ```

3. **Verify App.xaml ResourceDictionary**:
   ```xml
   <Application.Resources>
       <ResourceDictionary>
           <FontFamily x:Key="IconsFontFamily">MaterialIcons</FontFamily>
       </ResourceDictionary>
   </Application.Resources>
   ```

4. **Check XAML FontFamily reference**:
   ```xml
   <!-- Must match x:Key in App.xaml -->
   <FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                    Glyph="&#xE5D2;"
                    Color="White"
                    Size="34" />
   ```

**Solutions**:

**Option 1: Install Material Design Icons font**
```bash
# Download from Google Material Design Icons repository
curl -L -o Resources/Fonts/MaterialIcons-Regular.ttf \
  https://github.com/google/material-design-icons/raw/master/font/MaterialIcons-Regular.ttf
```

**Option 2: Use NuGet package**
```bash
dotnet add package MaterialDesign.Icons.Avalonia
```

**Option 3: Manual setup**
1. Download `MaterialIcons-Regular.ttf` from [Google Material Design Icons](https://github.com/google/material-design-icons)
2. Place in `Resources/Fonts/` directory
3. Add to `.csproj`:
   ```xml
   <MauiFont Include="Resources\Fonts\MaterialIcons-Regular.ttf" />
   ```
4. Configure in `MauiProgram.cs` (see above)
5. Add ResourceDictionary to `App.xaml` (see above)

---

### 3. Icons Render Incorrectly (Wrong Icon)

**Symptom**: Icon displays but is the wrong icon (e.g., hamburger menu shows as lightbulb).

**Root Cause**: Incorrect icon code or mapping error.

**Verification Steps**:

1. **Find icon code in Material Design Icons**:
   - Visit [Material Design Icons Search](https://fonts.google.com/icons)
   - Find desired icon
   - Copy codepoint (e.g., `e5d2` for menu icon)

2. **Verify Zeplin design data**:
   - Open design in Zeplin
   - Check icon element properties
   - Verify icon code matches Material Design codepoint

3. **Check conversion log**:
   ```typescript
   // If --verbose flag used, check conversion log
   Icon Conversion: &#xe5d2; -> &#xE5D2; (U+E5D2)
   ```

**Solutions**:

**Option 1: Update Zeplin design**
1. Fix icon code in Zeplin design
2. Re-run `/zeplin-to-maui` to regenerate

**Option 2: Manual correction**
1. Look up correct Material Design icon code
2. Update XAML Glyph attribute:
   ```xml
   <!-- Menu icon (hamburger) -->
   <FontImageSource Glyph="&#xE5D2;" ... />

   <!-- Lightbulb icon -->
   <FontImageSource Glyph="&#xE8B1;" ... />

   <!-- Label icon -->
   <FontImageSource Glyph="&#xE241;" ... />
   ```

**Reference**: [Material Design Icons Codepoints](https://github.com/google/material-design-icons/blob/master/font/MaterialIcons-Regular.codepoints)

---

### 4. Platform-Specific Rendering Issues

**Symptom**: Icons render correctly on one platform (e.g., Android) but not another (e.g., iOS).

**Common Causes**:
1. Font file not included for specific platform
2. Platform-specific font rendering differences
3. Icon size or color issues

**Platform-Specific Verification**:

**iOS**:
```bash
# Check font is included in iOS bundle
# In Xcode or Visual Studio, verify MaterialIcons-Regular.ttf in Resources
```

**Android**:
```bash
# Check font in Android resources
# Verify font file in obj/Debug/net8.0-android/assets
```

**Windows**:
```bash
# Check font installation on Windows platform
# Verify font file copied to app package
```

**Solutions**:

**Option 1: Verify font file paths**
```xml
<!-- In .csproj, ensure MauiFont includes all platforms -->
<MauiFont Include="Resources\Fonts\MaterialIcons-Regular.ttf" />
```

**Option 2: Add platform-specific font references**
```csharp
// In MauiProgram.cs
#if ANDROID
fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons");
#elif IOS
fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons");
#elif WINDOWS
fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons");
#endif
```

**Option 3: Use platform-specific icon size/color**
```xml
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xE5D2;"
                 Color="White">
    <FontImageSource.Size>
        <OnPlatform x:TypeArguments="x:Double">
            <On Platform="iOS" Value="28" />
            <On Platform="Android" Value="24" />
            <On Platform="WinUI" Value="32" />
        </OnPlatform>
    </FontImageSource.Size>
</FontImageSource>
```

---

### 5. Icon Code Validation Errors

**Symptom**: Icon converter reports validation errors or warnings.

**Example Error**:
```
⚠️ Icon Conversion Warning: Code point U+ZZZZ is outside Material Design Icons range (U+E000 to U+F8FF)
```

**Root Cause**: Icon code is outside the valid Material Design Icons Private Use Area range.

**Verification Steps**:

1. **Check if code is in valid range**:
   - Material Design Icons use Unicode Private Use Area
   - Valid range: U+E000 to U+F8FF
   - Example valid codes: U+E5D2, U+E8B1, U+E241

2. **Verify icon source**:
   - Ensure using Material Design Icons (not Font Awesome, Ionicons, etc.)
   - Check Zeplin design uses correct icon font

**Solutions**:

**Option 1: Use Material Design Icons**
1. Replace icon in Zeplin with Material Design equivalent
2. Re-extract design with `/zeplin-to-maui`

**Option 2: Use different icon font family**
1. Install alternative icon font (Font Awesome, Ionicons)
2. Update FontFamily in XAML
3. Update icon code format for that font family

**Option 3: Use SVG icons instead**
```xml
<!-- Alternative: Use SVG instead of font icons -->
<Image Source="menu_icon.svg"
       WidthRequest="24"
       HeightRequest="24" />
```

---

## Verification Steps

### Quick Icon Rendering Test

**1. Create test XAML**:
```xml
<ContentView xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml">
    <VerticalStackLayout Spacing="20" Padding="20">
        <!-- Menu icon (U+E5D2) -->
        <FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                         Glyph="&#xE5D2;"
                         Color="Black"
                         Size="48" />

        <!-- Lightbulb icon (U+E8B1) -->
        <FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                         Glyph="&#xE8B1;"
                         Color="Black"
                         Size="48" />

        <!-- Label icon (U+E241) -->
        <FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                         Glyph="&#xE241;"
                         Color="Black"
                         Size="48" />
    </VerticalStackLayout>
</ContentView>
```

**2. Expected Results**:
- ☰ (Menu/Hamburger icon)
- 💡 (Lightbulb icon)
- 🏷️ (Label icon)

**3. If icons don't render correctly**:
- Check font file exists (see Issue #2)
- Verify hex digits are uppercase (see Issue #1)
- Test on different platforms (see Issue #4)

---

## Manual Icon Code Conversion

If you need to manually convert icon codes:

### Conversion Formula

```
HTML Entity (lowercase) → XAML Format (uppercase)
&#xe5d2; → &#xE5D2;

Steps:
1. Take lowercase hex: e5d2
2. Convert to uppercase: E5D2
3. Wrap in XAML entity: &#xE5D2;
```

### Common Material Design Icon Codes

| Icon Name | Lowercase (Zeplin) | Uppercase (XAML) | Unicode |
|-----------|-------------------|------------------|---------|
| Menu (hamburger) | `&#xe5d2;` | `&#xE5D2;` | U+E5D2 |
| Lightbulb | `&#xe8b1;` | `&#xE8B1;` | U+E8B1 |
| Label | `&#xe241;` | `&#xE241;` | U+E241 |
| Check/Done | `&#xe86c;` | `&#xE86C;` | U+E86C |
| Error | `&#xe000;` | `&#xE000;` | U+E000 |
| Chevron Right | `&#xe5cc;` | `&#xE5CC;` | U+E5CC |
| Barcode Scanner | `&#xef4b;` | `&#xEF4B;` | U+EF4B |

### Online Conversion Tool

Use the icon converter utility:
```typescript
import { formatForXaml } from './utils/icon-converter';

const xamlCode = formatForXaml("&#xe5d2;");
console.log(xamlCode); // "&#xE5D2;"
```

---

## Prevention

### Best Practices to Avoid Icon Issues

1. **Use Zeplin-to-MAUI v1.1.0+**
   - Icon converter included by default
   - Automatic format conversion

2. **Verify Material Design Icons setup before generation**
   - Run `/mcp-zeplin verify` before `/zeplin-to-maui`
   - Check font file exists in project

3. **Use verbose mode for debugging**
   ```bash
   /zeplin-to-maui <url> --verbose
   ```

4. **Test on all target platforms**
   - Generate component
   - Test on iOS simulator
   - Test on Android emulator
   - Test on Windows (if applicable)

5. **Document icon requirements in Zeplin**
   - Tag icon elements as "icon"
   - Include icon code in design notes
   - Verify icon codes match Material Design Icons

---

## Getting Help

### Debug Information to Collect

When reporting icon rendering issues, include:

1. **Icon code from Zeplin**:
   ```
   Original icon code: &#xe5d2;
   ```

2. **Generated XAML snippet**:
   ```xml
   <FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                    Glyph="&#xe5d2;"
                    Color="White"
                    Size="34" />
   ```

3. **Platform and version**:
   ```
   Platform: iOS 17.0
   .NET MAUI: 8.0
   Device: iPhone 15 Simulator
   ```

4. **Font configuration**:
   ```csharp
   // From MauiProgram.cs
   fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons");
   ```

5. **Conversion log** (if using `--verbose`):
   ```
   Icon Conversion: &#xe5d2; -> &#xE5D2; (U+E5D2)
   Validation: PASSED (Material Design Icons range)
   ```

### Related Documentation

- [Icon Code Conversion Pattern](../patterns/icon-code-conversion-pattern.md)
- [Zeplin-to-MAUI Command Reference](../../installer/global/commands/zeplin-to-maui.md)
- [Material Design Icons Setup](https://fonts.google.com/icons)

---

**Last Updated**: 2025-10-16
**Version**: 1.0.0
