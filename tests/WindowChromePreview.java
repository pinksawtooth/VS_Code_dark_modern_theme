import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.file.Path;
import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.Border;
import com.formdev.flatlaf.FlatDarkLaf;
import generic.theme.*;

/** Offscreen palette samples, Ghidra tab borders and standard Swing tabs. */
public class WindowChromePreview {
    private static class PreviewThemeManager extends HeadlessThemeManager {
        PreviewThemeManager(GTheme theme) {
            currentValues = new GThemeValueMap(theme);
            GColor.refreshAll(currentValues);
            GIcon.refreshAll(currentValues);
        }
    }

    private static void layout(Container c) {
        c.doLayout();
        for (Component child : c.getComponents()) {
            if (child instanceof Container container) layout(container);
        }
    }

    private static void paint(Graphics2D g, JComponent component, int x, int y, int w, int h) {
        component.setSize(w, h);
        layout(component);
        Graphics2D copy = (Graphics2D) g.create(x, y, w, h);
        component.printAll(copy);
        copy.dispose();
    }

    private static JPanel ghidraTab(GTheme theme, String title, boolean selected) throws Exception {
        // GTabPanel needs a native drag cursor. Paint its actual border with
        // standard labels instead; no mouse/drag behavior is simulated here.
        var constructor = Class.forName("docking.widgets.tab.GTabBorder")
            .getDeclaredConstructor(boolean.class);
        constructor.setAccessible(true);
        JPanel tab = new JPanel(new BorderLayout(10, 0));
        tab.setBorder((Border) constructor.newInstance(selected));
        tab.setBackground(theme.getResolvedColor("color.bg.widget.tabs." +
            (selected ? "selected.active" : "unselected")));
        JLabel label = new JLabel(title);
        label.setFont(theme.getResolvedFont("font.widget.tabs"));
        label.setForeground(theme.getResolvedColor("color.fg.widget.tabs." +
            (selected ? "selected.active" : "unselected")));
        tab.add(label, BorderLayout.CENTER);
        tab.add(new JLabel(theme.getResolvedIcon("icon.widget.tabs.close")), BorderLayout.EAST);
        return tab;
    }

    private static JPanel headerSample(GTheme theme, String title, boolean selected) {
        // GenericHeader initializes native keyboard shortcuts even offscreen.
        // Reproduce only its title colors/gradient and fixed gray border here.
        String state = selected ? "active" : "inactive";
        Color start = theme.getResolvedColor("color.bg.header." + state);
        JPanel panel = new JPanel(new BorderLayout()) {
            @Override protected void paintComponent(Graphics graphics) {
                super.paintComponent(graphics);
                Graphics2D copy = (Graphics2D) graphics.create();
                copy.setPaint(new GradientPaint(100, 0, start, getWidth(), 0, getBackground()));
                copy.fillRect(0, 0, getWidth(), getHeight());
                copy.dispose();
            }
        };
        panel.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        JLabel label = new JLabel(title);
        label.setBorder(BorderFactory.createEmptyBorder(0, 6, 0, 0));
        label.setForeground(theme.getResolvedColor("color.fg.header." + state));
        panel.add(label, BorderLayout.CENTER);
        return panel;
    }

    public static void render(GTheme theme, Path output) throws Exception {
        UIManager.setLookAndFeel(new FlatDarkLaf());
        new PreviewThemeManager(theme);
        for (ColorValue color : theme.getColors()) {
            if (color.getId().startsWith("laf.color.")) {
                UIManager.put(color.getId().substring("laf.color.".length()), color.get(theme));
            }
        }
        for (JavaPropertyValue property : theme.getProperties()) {
            UIManager.put(property.getId(), property.get(theme));
        }
        UIManager.put("Label.font", theme.getResolvedFont("font.standard"));
        UIManager.put("Panel.font", theme.getResolvedFont("font.standard"));
        UIManager.put("TabbedPane.font", theme.getResolvedFont("font.standard"));

        BufferedImage result = new BufferedImage(1000, 425, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = result.createGraphics();
        g.setColor(theme.getResolvedColor("color.palette.vscode.chrome"));
        g.fillRect(0, 0, 1000, 425);
        g.setColor(theme.getResolvedColor("color.fg"));
        g.setFont(theme.getResolvedFont("font.standard").deriveFont(14f));
        g.drawString("Window chrome - offscreen component samples", 24, 28);
        g.drawString("Header color samples: focused / unfocused", 24, 65);
        for (int i = 0; i < 2; i++) {
            paint(g, headerSample(theme, i == 0 ? "Listing: sample.exe" : "Decompiler: entry",
                i == 0), 24 + i * 486, 80, 462, 28);
        }
        g.drawString("Ghidra document-tab borders (stock geometry retained)", 24, 145);
        paint(g, ghidraTab(theme, "sample.exe", true), 24, 160, 180, 28);
        paint(g, ghidraTab(theme, "library.dll", false), 204, 160, 180, 28);
        g.drawString("Standard Swing tabs / FlatLaf", 24, 230);
        JTabbedPane tabs = new JTabbedPane();
        tabs.addTab("Options", new JPanel());
        tabs.addTab("Display", new JPanel());
        tabs.addTab("Advanced", new JPanel());
        paint(g, tabs, 24, 245, 948, 76);
        g.drawString("Close: normal / hover", 24, 363);
        theme.getResolvedIcon("icon.widget.tabs.close").paintIcon(null, g, 194, 349);
        theme.getResolvedIcon("icon.widget.tabs.close.highlight").paintIcon(null, g, 229, 349);
        g.drawString("Tab list", 280, 363);
        theme.getResolvedIcon("icon.widget.tabs.list").paintIcon(null, g, 345, 349);
        g.drawString("Native OS title bars and drag/resize behavior are outside this offscreen preview.", 24, 404);
        g.dispose();
        ImageIO.write(result, "png", output.toFile());
    }
}
